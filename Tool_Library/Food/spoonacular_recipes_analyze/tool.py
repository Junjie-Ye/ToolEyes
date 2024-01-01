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


def autocomplete_recipe_search(
    query: str,
    number: int = 2,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/autocomplete"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "number": number
    }
    response = get_response(url, headers=headers, params=params)
    return response


def analyze_recipe(
    title: str,
    ingredients: list,
    instructions: str = None,
    servings: str = None,
    language: str = "en",
    includeNutrition: bool = False,
    includeTaste: bool = False,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/analyze"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "language": language,
        "includeNutrition": includeNutrition,
        "includeTaste": includeTaste
    }

    data = json.dumps({
        "title": title,
        "servings": servings,
        "ingredients": ingredients,
        "instructions": instructions
    })

    response = post_response(url, headers=headers, data=data, params=params)
    return response


def summarize_recipe(
    id: int,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/{id}/summary"

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }
    response = get_response(url, headers=headers, params=params)
    return response


def analyze_recipe_instructions(
    instructions: str,
    apiKey: str = ""
):
    url = f"https://api.spoonacular.com/recipes/analyzeInstructions"
    # print(instructions)

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }

    data = {
        "instructions": instructions
    }
    data = json.dumps(data)
    response = post_response(url, headers=headers, data=data, params=params)
    return response


def classify_cuisine(
    title: str,
    ingredientList: str,
    language: str = "en",
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/cuisine"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "title": title,
        "ingredientList": ingredientList,
        "language": language
    }
    data = {}

    response = post_response(url, headers=headers, params=params, data=data)
    return response


def analyze_a_recipe_search_query(
    q: str,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/queries/analyze"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "q": q
    }
    response = get_response(url, headers=headers, params=params)
    return response


def guess_nutrition_by_dish_name(
    title: str,
    apiKey: str = ""

):
    url = f"https://api.spoonacular.com/recipes/guessNutrition"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "title": title
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(autocomplete_recipe_search(query="chick"))
    # print(analyze_recipe())
    # print(summarize_recipe(4632))
    # print(classify_cuisine("Pork roast with green beans", "3 oz pork shoulder"))
    # print(guess_nutrition_by_dish_name("Spaghetti Aglio et Olio"))
    # print(analyze_recipe(title="Spaghetti Carbonara",
    #                      ingredients=["1 lb spaghetti","3.5 oz pancetta","2 Tbsps olive oil",],
    #                      instructions="Bring a large pot of water to a boil and season generously with salt. Add the pasta to the water once boiling and cook until al dente. Reserve 2 cups of cooking water and drain the pasta.",
    #                      servings=2))
    print(analyze_recipe_instructions(
        instructions="Put the garlic in a pan and then add the onion. Add some salt and oregano."))
    pass
