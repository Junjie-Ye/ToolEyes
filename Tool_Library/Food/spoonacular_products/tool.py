import requests
import json

# utils


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

# Tools


def search_grocery_products(
    query: str,
    apiKey: str = "",
    minCarbs: float = None,
    maxCarbs: float = None,
    minProtein: float = None,
    maxProtein: float = None,
    minCalories: float = None,
    maxCalories: float = None,
    minFat: float = None,
    maxFat: float = None,
    addProductInformation: bool = False,
    offset: int = None,
    number: int = 10,
):
    url = f"https://api.spoonacular.com/food/products/search"

    headers = {
        "x-api-key": apiKey
    }

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
        "addProductInformation": addProductInformation,
        "offset": offset,
        "number": number,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def search_grocery_products_by_UPC(
    upc: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/products/upc/{upc}"

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_product_information(
    id: int,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/products/{id}"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "id": id,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_comparable_products(
    upc: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/products/upc/{upc}/comparable"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "upc": upc,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def autocomplete_product_search(
    query: str,
    apiKey: str = "",
    number: int = None,
):
    url = f"https://api.spoonacular.com/food/products/suggest"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "number": number,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def classify_grocery_product(
    postbody: dict,
    apiKey: str = "",
    locale: str = "en-US",
):
    url = f"https://api.spoonacular.com/food/products/classify"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "locale": locale,
    }
    data = json.dumps(postbody)
    response = post_response(url, headers=headers, params=params, data=data)
    return response


def classify_grocery_product_bulk(
    postbody: list,
    apiKey: str = "",
    locale: str = "en-US",
):
    url = f"https://api.spoonacular.com/food/products/classifyBatch"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "locale": locale,
    }
    data = json.dumps(postbody)
    response = post_response(url, headers=headers, params=params, data=data)
    return response


def map_ingredients_to_grocery_products(
    postbody: list,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/ingredients/map"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    data = json.dumps(postbody)
    response = post_response(url, headers=headers, params=params, data=data)
    return response


if __name__ == "__main__":
    # print(search_grocery_products(query="pizza", number=2))
    # print(search_grocery_products_by_UPC(upc=041631000564))
    # print(get_product_information(id=22347))
    # print(get_comparable_products(upc="033698816271"))
    # print(autocomplete_product_search(query="chicke", number=2))
    # print(classify_grocery_product(postbody={"title": "chicken"}, locale="en-US"))
    # print(classify_grocery_product_bulk(postbody=[{ "title": "Kroger Vitamin A & D Reduced Fat 2% Milk", "upc": "", "plu_code": "" }]))
    print(map_ingredients_to_grocery_products(
        postbody={"ingredients": ["eggs", "bacon"], "servings": 2}))
    pass
