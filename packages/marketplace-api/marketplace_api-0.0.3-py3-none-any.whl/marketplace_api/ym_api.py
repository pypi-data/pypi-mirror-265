import json
import os
import time
from urllib.parse import urlparse

import pandas as pd
import requests
from pandas import DataFrame
from requests import Response


def exec_get_request(
    *,
    url: str,
    api_key: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str | int] | None = None,
) -> Response:
    if headers is None:
        headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
    if params is None:
        params = {}
    response = requests.get(url=url, headers=headers, params=params)
    return response


def exec_post_request(
    *,
    url: str,
    api_key: str,
    headers: dict[str, str] | None = None,
    data: dict[str, str | int] | str | None = None,
) -> Response:

    if headers is None:
        headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
    if data is None:
        data = json.dumps({})
    response = requests.post(url=url, headers=headers, data=data)
    return response


def get_warehouses(*, api_key: str) -> Response:
    """Возвращает список складов Маркета (FBY) с их идентификаторами.
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/warehouses/getFulfillmentWarehouses"""
    url: str = "https://api.partner.market.yandex.ru/warehouses?"
    response = exec_get_request(url=url, api_key=api_key)
    return response


def get_campaigns(*, api_key: str) -> Response:
    """Магазины пользователя
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/campaigns/getCampaigns"""
    url: str = "https://api.partner.market.yandex.ru/campaigns?"
    response = exec_get_request(api_key=api_key, url=url)
    return response


def download_report_file(*, api_key: str, report_id: str) -> str:
    """YM скачивание готовых отчетов
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/reports/getReportInfo"""
    url: str = f"https://api.partner.market.yandex.ru/reports/info/{report_id}"
    while True:  # проверим готовность отчета, если не готов в цикле повторяем проверку с задержкой в 1 сек
        r = exec_get_request(url=url, api_key=api_key)
        if not r:
            return r.text
        result = r.json()["result"]
        if result["status"] == "DONE":
            file_url = result["file"]
            break
        time.sleep(1)
    # получим имя файла по его url
    filename: str = os.path.basename(urlparse(file_url).path)
    # скачаем содержимое файла в двоичном режиме и сохраним в файл
    file_content = requests.get(file_url).content
    with open(filename, mode="wb") as file:
        file.write(file_content)
    # return r
    return filename


def get_sales_report(*, api_key: str, business_id: str, date_from: str, date_to: str) -> tuple[Response, DataFrame]:
    # TODO замени на работу с csv файлом
    """Отчет «Аналитика продаж»
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/reports/generateShowsSalesReport
    """
    url = f"https://api.partner.market.yandex.ru/reports/shows-sales/generate"
    data = json.dumps(
        {
            "businessId": business_id,
            "dateFrom": date_from,
            "dateTo": date_to,
            "grouping": "OFFERS",
        }
    )
    r = exec_post_request(url=url, api_key=api_key, data=data)
    report_id = r.json()["result"]["reportId"]
    download_report_file(api_key=api_key, report_id=report_id)
    df = pd.read_excel(f"{report_id}.xlsx")
    os.remove(f"{report_id}.xlsx")
    return r, df


def get_prices(*, api_key: str, campaing_id: str) -> Response:
    """Цены установленные в магазине
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/assortment/getPricesByOfferIds"""
    url = f"https://api.partner.market.yandex.ru/campaigns/{campaing_id}/offer-prices?"
    response = exec_post_request(url=url, api_key=api_key)
    return response


def get_prices_df(*, api_key: str, campaing_id: str) -> DataFrame:
    r = get_prices(api_key=api_key, campaing_id=campaing_id)

    data = r.json()
    offers = data["result"]["offers"]

    prices = []
    for offer in offers:
        br_id = offer["offerId"]
        price = offer["price"]["value"]
        prices.append((br_id, price))

    df = DataFrame(prices, columns=["id_br", "price"])
    return df


def get_stocks_batch(*, api_key: str, campaign_id: str, page_token: str = "") -> Response:
    """Получим Response данных с ценами
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/stocks/getStocks
    """
    r = exec_post_request(
        url=f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/offers/stocks?page_token={page_token}",
        api_key=api_key,
        data=json.dumps({"page_token": page_token}),
    )
    return r


def get_stocks(*, api_key: str, campaign_id: str) -> list[Response]:
    """Получим все Response данных с ценами и соединим их в список"""
    next_page_token = ""
    keep_running = True
    responses = []

    while keep_running:
        r = get_stocks_batch(api_key=api_key, campaign_id=campaign_id, page_token=next_page_token)
        responses.append(r)
        next_page_token = r.json()["result"]["paging"].get("nextPageToken")
        if not next_page_token:
            keep_running = False
    return responses


def get_stocks_df(*, api_key: str, campaign_id: str) -> DataFrame:
    """Конвертируем каждый Response с ценами в датафрейм и конкатенируем все датафреймы в один"""

    def conv_resp(response: Response) -> DataFrame:
        """Конвертируем отдельный Response с ценами в датафрейм"""
        data = response.json()
        warehouses = data["result"]["warehouses"]

        batch_wh_stocks: list[tuple[int, str, int]] = []
        for wh in warehouses:
            wh_i_id = wh["warehouseId"]
            wh_i_offers = wh["offers"]

            for i in wh_i_offers:
                br_id = i["offerId"]
                stocks = i["stocks"]
                for j in stocks:
                    # count = 0
                    if j.get("type") == "FIT":
                        count = j["count"]
                        batch_wh_stocks.append((wh_i_id, br_id, count))
        df = DataFrame(batch_wh_stocks, columns=["wh_id", "id_br", "stock"])
        return df

    rs: list[Response] = get_stocks(api_key=api_key, campaign_id=campaign_id)
    res_df = DataFrame()
    for r in rs:
        res_df = pd.concat([res_df, conv_resp(r)])

    return res_df


def get_orders_batch(*, api_key: str, campaign_id: str, date_from: str, date_to: str, page_token: str = "") -> Response:
    """Получим Response данных с заказами
    https://yandex.ru/dev/market/partner-api/doc/ru/reference/stats/getOrdersStats
    """
    r = exec_post_request(
        url=f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/stats/orders?page_token={page_token}&limit=200",
        api_key=api_key,
        data=json.dumps({"dateFrom": date_from, "dateTo": date_to}),
    )
    return r


def get_orders(*, api_key: str, campaign_id: str, date_from: str, date_to: str) -> list[Response]:
    """Получим все Response данных с заказами и соединим их в список"""
    next_page_token = ""
    keep_running = True
    responses: list[Response] = []

    while keep_running:
        r = get_orders_batch(api_key=api_key, campaign_id=campaign_id, date_from=date_from, date_to=date_to, page_token=next_page_token)
        if r.text == '{"status":"OK","result":{"orders":[],"paging":{}}}':
            keep_running = False
            return responses
        responses.append(r)
        next_page_token = r.json()["result"]["paging"].get("nextPageToken")
        if not next_page_token:
            keep_running = False
    return responses


def get_orders_df(*, api_key: str, campaign_id: str, date_from: str, date_to: str) -> DataFrame:
    """Конвертируем каждый Response с заказами в датафрейм и конкатенируем все датафреймы в один"""

    def conv_resp(response: Response) -> DataFrame:
        """Конвертируем отдельный Response с заказами в датафрейм"""
        data = response.json()
        df = DataFrame.from_dict(pd.json_normalize(data["result"]["orders"]), orient="columns")  # type: ignore[arg-type]
        # df = df.query('status not in ["CANCELLED_BEFORE_PROCESSING", "CANCELLED_IN_PROCESSING"]').reset_index(drop=True)
        df = df.query('status not in ["CANCELLED_BEFORE_PROCESSING"]').reset_index(drop=True)

        """ в датафрейме с заказами разобьем заказы с 2-мя и более id на отдельные строки"""
        orders_w_items = []
        for _, row in df.iterrows():
            items = row["items"]
            for item in items:
                br_id = item["shopSku"]
                count = item["count"]
                cost_per_item = sum([i["costPerItem"] for i in item["prices"]])
                item_price_full = sum([i["total"] for i in item["prices"]])

                item_dict = {
                    "order_id": row["id"],
                    "creationDate": row["creationDate"],
                    "status": row["status"],
                    "br_id": br_id,
                    "count": count,
                    "costPerItem": cost_per_item,
                    "item_price_full": item_price_full,
                }
                orders_w_items.append(item_dict)
        df = DataFrame.from_dict(orders_w_items)  # type: ignore[arg-type]
        return df

    rs: list[Response] = get_orders(api_key=api_key, campaign_id=campaign_id, date_from=date_from, date_to=date_to)
    res_df = DataFrame()
    for r in rs:
        res_df = pd.concat([res_df, conv_resp(r)])

    return res_df
