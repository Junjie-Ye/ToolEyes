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


def taste_by_id(
    id: int,
    normalize: bool = None,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/tasteWidget.json"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "normalize": normalize
    }
    response = get_response(url, headers=headers, params=params)
    return response


def equipment_by_id(
    id: int,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/equipmentWidget.json"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    response = get_response(url, headers=headers, params=params)
    return response


def price_breakdown_by_id(
    id: int,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/priceBreakdownWidget.json"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    response = get_response(url, headers=headers, params=params)
    return response


def ingredients_by_id(
    id: int,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/ingredientWidget.json"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    response = get_response(url, headers=headers, params=params)
    return response


def nutrition_by_id(
    id: int,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/nutritionWidget.json"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(taste_by_id(69095))
    # print(equipment_by_id(1003464))
    # print(price_breakdown_by_id(1003464))
    # print(ingredients_by_id(1003464))
    print(nutrition_by_id(324694))
    pass
