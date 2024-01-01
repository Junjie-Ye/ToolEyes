import requests
import json


def get_response(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def post_response(url, headers, params, data):
    response = requests.post(url, headers=headers, data=data, params=params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def search_menu_items(
    query: str,
    minCarbs: float = None,
    maxCarbs: float = None,
    minProtein: float = None,
    maxProtein: float = None,
    minCalories: float = None,
    maxCalories: float = None,
    minFat: float = None,
    maxFat: float = None,
    number: int = 10,
    addMenuItemInformation: bool = False,
    offset: int = 0,
    apiKey: str = "",
):
    url = "https://api.spoonacular.com/food/menuItems/search"
    params = {
        "query": query,
        "minCarbs": minCarbs,
        "maxCarbs": maxCarbs,
        "minProtein": minProtein,
        "maxProtein": maxProtein,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        "minFat": minFat,
        "maxFat": maxFat,
        "addMenuItemInformation": addMenuItemInformation,
        "offset": offset,
        "number": number
    }
    headers = {
        "x-api-key": apiKey
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_menu_item_info(
    id: int,
    apiKey: str = ""
):
    url = f"https://api.spoonacular.com/food/menuItems/{str(id)}"

    querystring = {}
    headers = {
        "x-api-key": apiKey
    }

    response = get_response(url, headers=headers, params=querystring)
    return response


def autocomplete_menu_item_search(
    query_str: str,
    number: int = 2,
    apiKey: str = ""
):
    url = "https://api.spoonacular.com/food/menuItems/suggest"
    params = {
        "query": query_str,
        "number": number
    }

    headers = {
        "x-api-key": apiKey
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(get_menu_item_info(424571))
    print(search_menu_items(query_str="burger", number=2))
    # print(autocomplete_menu_item_search(query_str='chicke'))
    pass
