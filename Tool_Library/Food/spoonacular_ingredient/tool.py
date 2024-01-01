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
def ingredient_search(
    query: str,
    apiKey: str = "",
    addChildren: bool = False,
    minProteinPercent: int = None,
    maxProteinPercent: int = None,
    minFatPercent: int = None,
    maxFatPercent: int = None,
    minCarbsPercent: int = None,
    maxCarbsPercent: int = None,
    metaInformation: bool = False,
    intolerances: str = None,
    sort: str = None,
    sortDirection: str = None,
    language: str = None,
    offset: int = None,
    number: int = 10,
):
    url = f"https://api.spoonacular.com/food/ingredients/search"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "addChildren": addChildren,
        "minProteinPercent": minProteinPercent,
        "maxProteinPercent": maxProteinPercent,
        "minFatPercent": minFatPercent,
        "maxFatPercent": maxFatPercent,
        "minCarbsPercent": minCarbsPercent,
        "maxCarbsPercent": maxCarbsPercent,
        "metaInformation": metaInformation,
        "intolerances": intolerances,
        "sort": sort,
        "sortDirection": sortDirection,
        "language": language,
        "offset": offset,
        "number": number,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def get_ingredient_information(
    id: int,
    apiKey: str = "",
    amount: int = None,
    unit: str = None,
):
    url = f"https://api.spoonacular.com/food/ingredients/{id}/information"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "amount": amount,
        "unit": unit,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def compute_ingredient_amount(
    id: int,
    nutrient: str,
    target: int,
    apiKey: str = "",
    unit: str = None,
):
    url = f"https://api.spoonacular.com/food/ingredients/{id}/amount"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "nutrient": nutrient,
        "target": target,
        "unit": unit,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def convert_amounts(
    ingredientName: str,
    sourceAmount: float,
    sourceUnit: str,
    targetUnit: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/recipes/convert"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "ingredientName": ingredientName,
        "sourceAmount": sourceAmount,
        "sourceUnit": sourceUnit,
        "targetUnit": targetUnit,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def parse_ingredients(
    ingredientList: str,
    servings: int,
    includeNutrition: bool,
    language: str = "en",
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/recipes/parseIngredients"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "language": language,
    }
    data = {
        "ingredientList": ingredientList,
        "servings": servings,
        "includeNutrition": includeNutrition,
    }
    response = post_response(url, headers=headers, params=params, data=data)
    return response

def compute_glycemic_load(
    postbody: dict,
    language: str = "en",
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/ingredients/glycemicLoad"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "language": language,
    }
    data = json.dumps(postbody)
    response = post_response(url, headers=headers, params=params, data=data)
    return response

def autocomplete_ingredient_search(
    query: str,
    number: int = None,
    language: str = "en",
    metaInformation: bool = False,
    intolerances: str = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/ingredients/autocomplete"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "number": number,
        "language": language,
        "metaInformation": metaInformation,
        "intolerances": intolerances,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def get_ingredient_substitutes(
    ingredientName: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/ingredients/substitutes"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "ingredientName": ingredientName,
    }
    response = get_response(url, headers=headers, params=params)
    return response

def get_ingredient_substitutes_by_id(
    id: int,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/ingredients/{id}/substitutes"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "id": id,
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(ingredient_search(query="apple", number=2, sort="calories", sortDirection="desc"))
    # print(get_ingredient_information(id=9266, amount=1))
    # print(compute_ingredient_amount(id=9266, nutrient="protein", target=10, unit="oz"))
    # print(convert_amounts(ingredientName="flour", sourceAmount=2.5, sourceUnit="cups", targetUnit="grams"))
    # print(parse_ingredients(ingredientList="1 cup green tea", servings=1, includeNutrition=True))
    # print(compute_glycemic_load(postbody={ "ingredients":[ "1 kiwi", "2 cups rice", "2 glasses of water" ] }))
    # print(autocomplete_ingredient_search(query="appl", number=2))
    # print(get_ingredient_substitutes(ingredientName="butter"))
    print(get_ingredient_substitutes_by_id(id=1001))
    pass
