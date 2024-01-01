import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_food_item_by_id(
    fdcId: str,
    nutrients: list[int] = None,
    format: str = None,
    api_key: str = "",
):
    headers = {"X-Api-Key": api_key, "accept": "application/json"}

    params = {"nutrients": nutrients, "format": format, "limit": "1"}
    url = f" https://api.nal.usda.gov/fdc/v1/food/{fdcId}"
    return get_response(url, headers, **params)


def get_multiple_food_items_by_ids(
    fdcIds: list[str],
    format: str = None,
    nutrients: list[int] = None,
    api_key: str = "",
):
    url = "https://api.nal.usda.gov/fdc/v1/foods"
    headers = {
        "X-Api-Key": api_key,
        "accept": "application/json",
    }
    params = {"fdcIds": fdcIds, "format": format, "nutrients": nutrients}
    return get_response(url, headers, **params)


def get_food_lists(
    dataType: list[str] = None,
    pageSize: int = 50,
    pageNumber: int = 2,
    sortBy: str = None,
    sortOrder: str = None,
    api_key: str = "",
):
    url = "https://api.nal.usda.gov/fdc/v1/foods/list"
    headers = {
        "X-Api-Key": api_key,
        "accept": "application/json",
    }
    params = {
        "dataType": dataType,
        "pageSize": pageSize,
        "pageNumber": pageNumber,
        "sortBy": sortBy,
        "sortOrder": sortOrder,
    }
    return get_response(url, headers, **params)


def search_foods(
    query: str,
    dataType: list[str] = None,
    pageSize: int = 50,
    pageNumber: int = 2,
    sortBy: str = None,
    sortOrder: str = None,
    brandOwner: str = None,
    api_key: str = "",
):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    headers = {
        "X-Api-Key": api_key,
        "accept": "application/json",
    }
    params = {
        "query": query,
        "dataType": dataType,
        "pageSize": pageSize,
        "pageNumber": pageNumber,
        "sortBy": sortBy,
        "sortOrder": sortOrder,
        "brandOwner": brandOwner,
    }
    return get_response(url, headers, **params)


if __name__ == "__main__":
    # print(get_food_item_by_id("534358", nutrients=[203, 204, 205]))
    # print(get_multiple_food_items_by_ids(["534358", "534359"]))
    # print(get_food_lists(dataType=["Branded"], pageSize=2, pageNumber=1))
    # print(search_foods("cheddar cheese", dataType=["Branded"], pageSize=2, pageNumber=1, sortBy="dataType.keyword", sortOrder="desc"))
    pass
