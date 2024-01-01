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


def search_all_food(
    query: str = None,
    offset: int = None,
    number: int = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/search"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "offset": offset,
        "number": number
    }
    response = get_response(url, headers=headers, params=params)
    return response

# TODO: cannot upload image


def image_classification_by_file(
    file: bin,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/images/classify"

    headers = {
        "x-api-key": apiKey
    }

    params = {}
    response = post_response(url, headers=headers, params=params)
    return response

# FIXME: Could not classify image


def image_classification_by_url(
    imageUrl: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/images/classify"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "imageUrl": imageUrl
    }
    response = get_response(url, headers=headers, params=params)
    return response

# FIXME: Could not analyze food image


def image_analysis_by_url(
    imageUrl: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/images/analyze"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "imageUrl": imageUrl
    }
    response = get_response(url, headers=headers, params=params)
    return response


def search_food_videos(
    query: str,
    type: str = None,
    cuisine: str = None,
    diet: str = None,
    includeIngredients: str = None,
    excludeIngredients: str = None,
    minLength: int = None,
    maxLength: int = None,
    offset: int = None,
    number: int = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/videos/search"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "type": type,
        "cuisine": cuisine,
        "diet": diet,
        "includeIngredients": includeIngredients,
        "excludeIngredients": excludeIngredients,
        "minLength": minLength,
        "maxLength": maxLength,
        "offset": offset,
        "number": number
    }
    response = get_response(url, headers=headers, params=params)
    return response


def quick_answer(
    q: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/recipes/quickAnswer"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "q": q,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def detect_food_in_text(
    text: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/detect"

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }
    data = {
        "text": text
    }
    response = post_response(url, headers=headers, params=params, data=data)
    return response


def search_site_content(
    query: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/site/search"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query
    }
    response = get_response(url, headers=headers, params=params)
    return response


def random_food_joke(
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/jokes/random"

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }
    response = get_response(url, headers=headers, params=params)
    return response


def random_food_trivia(
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/trivia/random"

    headers = {
        "x-api-key": apiKey
    }

    params = {
    }
    response = get_response(url, headers=headers, params=params)
    return response


def talk_to_chatbot(
    text: str,
    contextId: str = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/converse"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "text": text,
        "contextId": contextId
    }
    response = get_response(url, headers=headers, params=params)
    return response


def conversation_suggests(
    query: str,
    number: int,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/converse/suggest"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "number": number
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(search_all_food(query="apple", number=2))
    # print(image_classification_by_url(imageUrl="https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"))
    # print(image_analysis_by_url(imageUrl="https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"))
    # print(search_food_videos(query="apple", number=2))
    # print(quick_answer(q="How much vitamin c is in 2 apples?"))
    print(detect_food_in_text(text="I like to eat delicious tacos. The only thing better is a cheeseburger with cheddar. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good too!"))
    # print(search_site_content(query="past"))
    # print(random_food_joke())
    # print(random_food_trivia())
    # print(talk_to_chatbot(text="I want to eat an apple"))
    # print(conversation_suggests(query="tell", number=2))
    pass
