import requests


def get_response(url, headers=None, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


def random_cold_jokes():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    return get_response(url, headers=headers)
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助


def search_cold_jokes():
    url = "https://icanhazdadjoke.com/search"
    headers = {"Accept": "application/json"}
    return get_response(url, headers=headers)


def get_specific_cold_jokes(joke_id: str):
    url = f"https://icanhazdadjoke.com/j/{joke_id}"
    headers = {"Accept": "application/json"}
    return get_response(url, headers=headers)


def random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    return get_response(url)


def random_ten_joke():
    url = "https://official-joke-api.appspot.com/random_ten"
    return get_response(url)


def get_joke_by_id(id: str):
    url = f"https://official-joke-api.appspot.com/jokes/:{id}"
    return get_response(url)


def random_quote(lang_code: enumerate = None, api_key: enumerate = ""):
    url = "https://quotes15.p.rapidapi.com/quotes/random/"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "quotes15.p.rapidapi.com"
    }
    params = {'language_code': lang_code}
    response = get_response(url, headers=headers, **params)
    return (response)


if __name__ == '__main__':
    print(random_cold_jokes())
    print(search_cold_jokes())
    print(get_specific_cold_jokes('0189hNRf2g'))
    print(random_joke())
    print(random_ten_joke())
    print(get_joke_by_id("146"))
    print(random_quote(lang_code="en"))
