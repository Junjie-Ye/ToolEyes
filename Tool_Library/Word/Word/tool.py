import requests


def get_response(url: str, headers):
    try:
        response = requests.get(url=url, headers=headers)
    except:
        return {"error": "connection error."}

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


def get_definition(word: str, api_key: str = ''):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}'
    return get_response(url, headers)


def get_synonyms(word: str, api_key: str = ''):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    return get_response(url, headers)


def get_antonyms(word: str, api_key: str = ''):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/antonyms'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    return get_response(url, headers)


def get_examples(word: str, api_key: str = ''):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/examples'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    return get_response(url, headers)


def get_pronunciation(word: str, api_key: str = ''):
    observation = get_definition(word)
    return observation['pronunciation']


def get_rhymes(word: str, api_key: str = ''):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/rhymes'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    return get_response(url, headers)


def get_frequency(word: str, api_key: str = ''):
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/frequency'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    return get_response(url, headers)


def search_word(api_key: str = '', **kargs):
    url = 'https://wordapiv1.p.rapidapi.com/words'
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }
    try:
        response = requests.get(url=url, headers=headers, params=kargs)
    except:
        return {"error": "connection error."}

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


if __name__ == '__main__':
    # print(get_definition("type"))
    # print(get_synonyms("hello"))
    # print(get_antonyms("good"))
    # print(get_examples('hello'))
    # print(get_pronunciation('effect'))
    # print(get_rhymes('dog'))
    # print(get_frequency('hello'))
    # print(search_word(letterPattern='^a.{4}$'))
    # print(search_word(letters=6))
    # print(search_word(get_pronunciationPattern='.*æm$'))
    # print(search_word(sounds=4, limit=1))
    # print(search_word(random=True, limit=1))
    pass
