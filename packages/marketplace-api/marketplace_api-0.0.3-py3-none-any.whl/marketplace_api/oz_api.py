import json

import pandas as pd
import requests

from .utils import retry


# from .utils import retry


def exec_post_request(
    *,
    url: str,
    client_id: str,
    api_key: str,
    headers: dict[str, str] | None = None,
    data: dict[str, str | int] | str | None = None,
) -> requests.Response:
    if headers is None:
        headers = {"Content-Type": "application/json", "Client-Id": client_id, "Api-Key": api_key}
    data = json.dumps(data) if data else json.dumps({})
    response = requests.post(url=url, headers=headers, data=data)

    return response


def get_product_list(*, client_id: str, api_key: str, last_id: str | None = None) -> requests.Response:
    """Список товаров https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductList"""
    url = "https://api-seller.ozon.ru/v2/product/list"
    if last_id is not None:
        response = exec_post_request(url=url, client_id=client_id, api_key=api_key, data={"last_id": last_id})
    else:
        response = exec_post_request(url=url, client_id=client_id, api_key=api_key)
    return response


def get_full_product_list_df(*, client_id: str, api_key: str) -> pd.DataFrame:
    df_res = pd.DataFrame()
    last_id = None
    while True:
        r = get_product_list(client_id=client_id, api_key=api_key, last_id=last_id)
        data = r.json()["result"]["items"]
        last_id = r.json()["result"]["last_id"]
        df = pd.DataFrame.from_dict(pd.json_normalize(data), orient="columns")  # type: ignore
        df_res = pd.concat([df_res, df])
        if df.shape[0] < 1000:
            break

    return df_res


"""
Данные аналитики
https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_AnalyticsGetData
"""


def get_oz_analytics_data(
    *,
    api_key: str,
    client_id: str,
    date_from: str,
    date_to: str,
    metrics: list[str],
    dimension: list[str],
    filters: list[dict[str, str]],
    sort: list[dict[str, str]],
    limit: int = 1000,
    offset: int = 0,
) -> requests.Response:
    # https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_AnalyticsGetData
    response = requests.post(
        "https://api-seller.ozon.ru/v1/analytics/data",
        headers={
            "Content-Type": "application/json",
            "Client-Id": client_id,
            "Api-Key": api_key,
        },
        data=json.dumps(
            {
                "date_from": date_from,
                "date_to": date_to,
                "metrics": metrics,
                "dimension": dimension,
                "filters": filters,
                "sort": sort,
                "limit": limit,
                "offset": offset,
            }
        ),
    )
    return response


@retry(num_retries=10, exception_to_check=Exception, sleep_time=30)
def get_oz_analytics_data_df(
    *,
    api_key: str,
    client_id: str,
    date_from: str,
    date_to: str,
    metrics: list[str],
    dimension: list[str],
    filters: list[dict[str, str]],
    sort: list[dict[str, str]],
    limit: int = 1000,
    offset: int = 0,
) -> pd.DataFrame:
    r = get_oz_analytics_data(
        api_key=api_key,
        client_id=client_id,
        date_from=date_from,
        date_to=date_to,
        metrics=metrics,
        dimension=dimension,
        filters=filters,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    if not r:
        print(r.status_code, r.text)
        raise Exception(r.text)

    print(r.status_code, end=" ")
    data = r.json()["result"]["data"]

    return pd.DataFrame.from_dict(pd.json_normalize(data), orient="columns")  # type: ignore


def get_oz_analytics_data_all_df(
    *,
    api_key: str,
    client_id: str,
    date_from: str,
    date_to: str,
    metrics: list[str],
    dimension: list[str],
    filters: list[dict[str, str]] = (),  # type: ignore
    sort: list[dict[str, str]] = (),  # type: ignore
    limit: int = 1000,
) -> pd.DataFrame:
    df_all = pd.DataFrame()
    offset = 0
    while True:
        df_batch = get_oz_analytics_data_df(
            api_key=api_key,
            client_id=client_id,
            date_from=date_from,
            date_to=date_to,
            metrics=metrics,
            dimension=dimension,
            filters=filters,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        print(df_batch.shape, offset)
        offset += limit
        df_all = pd.concat([df_all, df_batch], ignore_index=True)
        if df_batch.shape[0] < limit:
            break

    df_all["dt"] = df_all["dimensions"].apply(lambda x: x[1]["id"])
    df_all["id_oz"] = df_all["dimensions"].apply(lambda x: x[0]["id"])

    for i, metric in enumerate(metrics):
        df_all[metric] = df_all["metrics"].apply(lambda x: x[i])

    df_all = df_all.drop(columns=["dimensions", "metrics"])

    return df_all


# df = get_oz_analytics_data_all_df(
#     api_key=OZ_API_KEY,
#     client_id=OZ_CLIENT_ID,
#     metrics=["ordered_units", "revenue"],
#     dimension=["sku", "day"],
#     date_from="2024-02-26",
#     date_to="2024-03-23",
#     filters=[{"key": "revenue", "op": "GT", "value": "0"}],
# )
