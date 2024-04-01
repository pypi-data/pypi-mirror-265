import itertools
import json

import requests
from requests import Response

# from ds82.common_utils import retry
from tqdm.auto import tqdm

from marketplace_api.utils import retry


def exec_get_request(
    *,
    url: str,
    api_key: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str | int] | None = None,
) -> Response:
    if headers is None:
        headers = {"Accept": "application/json", "Authorization": api_key}
    if params is None:
        params = {}
    response = requests.get(url=url, headers=headers, params=params)
    return response


# url = 'https://advert-api.wb.ru/adv/v1/promotion/count?'
# api_key = creds.get('WB_API_KEY')
# r = exec_get_request(url=url, api_key=api_key)
# print(r.text)


def exec_post_request(
    *,
    url: str,
    api_key: str,
    headers: dict[str, str] | None = None,
    data: dict[str, str | int] | str | None = None,
) -> Response:
    if headers is None:
        headers = {"Content-type": "application/json", "Accept": "application/json", "Authorization": api_key}
    if data is None:
        data = json.dumps({})
    response = requests.post(url=url, headers=headers, data=data)
    return response


def get_cards_list_descr(
    api_key: str,
    updated_at: str | None = None,
    nm_id: int | None = None,
) -> Response:  # TODO cover by tests
    """Список номенклатур (НМ)
    https://openapi.wb.ru/content/api/ru/#tag/Prosmotr/paths/~1content~1v2~1get~1cards~1list/post
    """
    url = "https://suppliers-api.wildberries.ru/content/v2/get/cards/list"
    data = json.dumps(
        {
            "settings": {
                "cursor": {
                    "limit": 1000,
                    "updatedAt": updated_at,
                    "nmID": nm_id,
                },
                "filter": {"withPhoto": -1},
            }
        }
    )
    r = exec_post_request(url=url, api_key=api_key, data=data)
    return r


def get_cards_list_descr_all(*, api_key: str) -> list[Response]:  # TODO cover by tests
    """ВЕСЬ Список номенклатур (НМ)
    Берем get_cards_list()
    (Список номенклатур (НМ)     https://openapi.wb.ru/content/api/ru/#tag/Prosmotr/paths/~1content~1v2~1get~1cards~1list/post)
    и складываем респонсы с учетом пагинации в список
    Вернет список респонсов
    """
    updated_at = None
    nm_id = None

    rs = []
    # for i in tqdm(itertools.count()):
    for i in itertools.count():
        r = get_cards_list_descr(api_key=api_key, updated_at=updated_at, nm_id=nm_id)
        rd = r.json()

        total = rd["cursor"]["total"]
        updated_at = rd["cursor"]["updatedAt"]
        nm_id = rd["cursor"]["nmID"]
        rs.append(r)
        if total < 1000:
            break
    return rs


# from config import creds
# a = get_cards_list_descr_all(api_key=creds['WB_API_KEY'])
# print(a[1].json()['cursor'])


@retry(num_retries=10, exception_to_check=Exception, sleep_time=5)  # type: ignore[misc, no-untyped-call]
def get_product_rating(api_key: str, id_wb: int) -> dict[str, int]:
    """Средняя оценка товара по артикулу WB на текущую дату
    https://openapi.wb.ru/feedbacks-questions/api/ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating~1nmid/get
    """
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/nmid?"
    headers = {"Accept": "application/json", "Authorization": api_key}
    params = {"nmId": id_wb}
    response = requests.get(url=url, headers=headers, params=params)

    data = response.json()
    if data["error"]:
        print(data)
        return {"error": data["errorText"], "additionalErrors": data["additionalErrors"]}

    rating = data["data"]["valuation"]
    feedbacks_count = data["data"]["feedbacksCount"]
    return {"id_wb": id_wb, "rating": rating, "feedbacksCount": feedbacks_count}


def get_product_rating_all(*, api_key: str, id_list: list[int]) -> list[dict[str, int]]:
    res = []
    # for id_wb in id_list:
    for id_wb in tqdm(id_list):
        data = get_product_rating(api_key, id_wb)
        if not data.get("error") and data["rating"]:
            res.append(data)
        else:
            # print(f'ups {id_wb}: {data = }')
            pass
    return res


# print("run requests")
# ratings = get_product_rating_all(api_key=creds["WB_API_KEY"], id_list=[159520614, 159520615])
# print(f"{len(ratings) = }")  # 856
# df = pd.DataFrame(ratings)
# print(df)
