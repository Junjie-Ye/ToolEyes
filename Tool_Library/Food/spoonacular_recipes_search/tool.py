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


def search_recipes(
    query: str,
    apiKey: str = "",
    cuisine: str = None,
    diet: str = None,
    intolerances: str = None,
    equipment: str = None,
    includeIngredients: str = None,
    excludeIngredients: str = None,
    type: str = None,
    instructionsRequired: bool = None,
    fillIngredients: bool = None,
    addRecipeInformation: bool = None,
    addRecipeNutrition: bool = None,
    author: str = None,
    tags: str = None,
    recipeBoxId: str = None,
    titleMatch: str = None,
    maxReadyTime: int = None,
    ignorePantry: bool = None,
    sort: str = None,
    sortDirection: str = None,
    minCarbs: float = None,
    maxCarbs: float = None,
    maxFat: float = None,
    number: int = 10,
    limitLicense: bool = False,
):
    url = f"https://api.spoonacular.com/recipes/complexSearch"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "cuisine": cuisine,
        "diet": diet,
        "intolerances": intolerances,
        "equipment": equipment,
        "includeIngredients": includeIngredients,
        "excludeIngredients": excludeIngredients,
        "type": type,
        "instructionsRequired": instructionsRequired,
        "fillIngredients": fillIngredients,
        "addRecipeInformation": addRecipeInformation,
        "addRecipeNutrition": addRecipeNutrition,
        "author": author,
        "tags": tags,
        "recipeBoxId": recipeBoxId,
        "titleMatch": titleMatch,
        "maxReadyTime": maxReadyTime,
        "ignorePantry": ignorePantry,
        "sort": sort,
        "sortDirection": sortDirection,
        "minCarbs": minCarbs,
        "maxCarbs": maxCarbs,
        "maxFat": maxFat,
        "number": number,
        "limitLicense": limitLicense
    }
    response = get_response(url, headers=headers, params=params)
    return response


def search_recipes_by_nutrients(
    apiKey: str = "",
    minCarbs: float = None,
    maxCarbs: float = None,
    minProtein: float = None,
    maxProtein: float = None,
    minCalories: float = None,
    maxCalories: float = None,
    minFat: float = None,
    maxFat: float = None,
    number: int = 10,
    random: bool = None,
    limitLicense: bool = False,
):
    url = f"https://api.spoonacular.com/recipes/findByNutrients"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "minCarbs": minCarbs,
        "maxCarbs": maxCarbs,
        "minProtein": minProtein,
        "maxProtein": maxProtein,
        "minCalories": minCalories,
        "maxCalories": maxCalories,
        "minFat": minFat,
        "maxFat": maxFat,
        "number": number,
        "random": random,
        "limitLicense": limitLicense
    }
    response = get_response(url, headers=headers, params=params)
    return response


def search_recipes_by_ingredients(
    ingredients: str,
    apiKey: str = "",
    number: int = 10,
    ranking: int = None,
    limitLicense: bool = False,
    ignorePantry: bool = None
):
    url = f"https://api.spoonacular.com/recipes/findByIngredients"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "ingredients": ingredients,
        "number": number,
        "ranking": ranking,
        "limitLicense": limitLicense,
        "ignorePantry": ignorePantry
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(search_recipes(query="chicken", maxFat=25, number=2))
    # print(search_recipes_by_nutrients(minCarbs=10, maxCarbs=50, number=2))
    print(search_recipes_by_ingredients(
        ingredients="apples,flour,sugar", number=2))
    pass
