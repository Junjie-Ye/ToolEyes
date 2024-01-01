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


def get_recipe_information(
    id: int,
    includeNutrition: bool = None,
    apiKey: str = ""
):
    url = f"https://api.spoonacular.com/recipes/{id}/information"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "includeNutrition": includeNutrition
    }

    response = get_response(url, headers=headers, params=params)
    return response


def get_recipe_information_bulk(
    ids: str,
    includeNutrition: bool = None,
    apiKey: str = ""
):
    url = f"https://api.spoonacular.com/recipes/informationBulk"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "ids": ids,  # "716429,716429,716429"
        "includeNutrition": includeNutrition
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_similar_recipes(
    id: int,
    number: int = None,
    limitLicense: bool = False,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/similar"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "number": number,
        "limitLicense": limitLicense
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_random_recipes(
    limitLicense: bool = False,
    tags: str = None,
    number: int = None,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/random"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "limitLicense": limitLicense,
        "tags": tags,
        "number": number
    }
    response = get_response(url, headers=headers, params=params)
    return response


def get_analyzed_recipe_instructions(
    id: int,
    stepBreakdown: bool = None,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "stepBreakdown": stepBreakdown
    }
    response = get_response(url, headers=headers, params=params)
    return response

# ERROR: Please use the 'Save to recipe box' button on the recipe page to save recipes from spoonacular.com.


def extract_recipe_from_website(
    url: str,
    forceExtraction: bool = None,
    analyze: bool = None,
    includeNutrition: bool = None,
    includeTaste: bool = None,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/extract"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "url": url,
        "forceExtraction": forceExtraction,
        "analyze": analyze,
        "includeNutrition": includeNutrition,
        "includeTaste": includeTaste
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(get_recipe_information(716429))
    # print(get_recipe_information_bulk("715538,716429"))
    # print(get_similar_recipes(715538))
    print(get_random_recipes())
    # print(autocomplete_recipe_search(query="chick"))
    # print(extract_recipe_from_website("https://foodista.com/recipe/ZHK4KPB6/chocolate-crinkle-cookies"))
    pass
