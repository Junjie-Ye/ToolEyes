import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_auto_suggestion(
    prefix: str,
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/recipes/auto-complete"
    headers = {"X-RapidAPI-Key": api_key,
               "X-RapidAPI-Host": "tasty.p.rapidapi.com"}

    params = {"prefix": prefix}

    return get_response(url, headers, **params)


def get_recipes(
    from_: int,
    size: int,
    api_key: str = "",
    tags: str = "",
    q: str = "",
    sort: str = "",
):
    url = "https://tasty.p.rapidapi.com/recipes/list"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tasty.p.rapidapi.com",
    }
    params = {"from": from_, "size": size, "tags": tags, "q": q, "sort": sort}

    return get_response(url, headers, **params)


def get_similar_recipes(
    id: int,
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/recipes/list-similarities"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tasty.p.rapidapi.com",
    }
    params = {"recipe_id": id}

    return get_response(url, headers, **params)


def get_more_info(
    id: int,
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tasty.p.rapidapi.com",
    }
    params = {"id": id}

    return get_response(url, headers, **params)


def load_tips(
    id: int,
    from_: int = 0,
    size: int = 30,
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/tips/list"

    params = {"id": id, "from": from_, "size": size}

    headers = {"X-RapidAPI-Key": api_key,
               "X-RapidAPI-Host": "tasty.p.rapidapi.com"}
    return get_response(url, headers, **params)


def list_tags(
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/tags/list"
    headers = {"X-RapidAPI-Key": api_key,
               "X-RapidAPI-Host": "tasty.p.rapidapi.com"}
    return get_response(url, headers)


def list_feeds(
    from_: int,
    size: int,
    timezone: str,
    vegetarian: bool,
    api_key: str = "",
):
    url = "https://tasty.p.rapidapi.com/feeds/list"

    params = {
        "size": size,
        "timezone": timezone,
        "vegetarian": vegetarian,
        "from": from_,
    }

    headers = {"X-RapidAPI-Key": api_key,
               "X-RapidAPI-Host": "tasty.p.rapidapi.com"}
    return get_response(url, headers, **params)


if __name__ == "__main__":
    # print(get_auto_suggestion("chicken soup"))
    # print(get_recipes(0, 10))
    # print(get_similar_recipes(123))
    # print(get_more_info(123))
    # print(load_tips(123,0,5))
    # print(list_tags())
    # print(list_feeds(0, 5, "+0700", True))
    pass
