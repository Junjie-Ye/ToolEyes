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


def search_restaurants(
    query: str = None,
    lat: float = None,
    lng: float = None,
    distance: int = None,
    budget: int = None,
    cuisine: str = None,
    min_rating: float = None,
    is_open: bool = None,
    sort: str = None,
    page: int = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/restaurants/search"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "query": query,
        "lat": lat,
        "lng": lng,
        "distance": distance,
        "budget": budget,
        "cuisine": cuisine,
        "min-rating": min_rating,
        "is-open": is_open,
        "sort": sort,
        "page": page,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def dish_pairing_for_wine(
    wine: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/wine/dishes"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "wine": wine,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def wine_pairing(
    food: str,
    maxPrice: int = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/wine/pairing"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "food": food,
        "maxPrice": maxPrice,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def wine_description(
    wine: str,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/wine/description"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "wine": wine,
    }
    response = get_response(url, headers=headers, params=params)
    return response


def wine_recommendation(
    wine: str,
    maxPrice: int = None,
    minRating: float = None,
    number: int = None,
    apiKey: str = "",
):
    url = f"https://api.spoonacular.com/food/wine/recommendation"

    headers = {
        "x-api-key": apiKey
    }

    params = {
        "wine": wine,
    }
    response = get_response(url, headers=headers, params=params)
    return response


if __name__ == "__main__":
    # print(search_restaurants(query="beach cafe", lat=37.7786357, lng=-122.3918135, budget=20))
    # print(dish_pairing_for_wine(wine="malbec"))
    # print(wine_pairing(food="steak"))
    # print(wine_description(wine="merlot"))
    print(wine_recommendation(wine="merlot", number=2))
    pass
