import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def random_advice():
    url = '	https://api.adviceslip.com/advice'

    return get_response(url)


def advice_by_id(slip_id:int):
    url = f'https://api.adviceslip.com/advice/{slip_id}'

    return get_response(url)


def search_advice(query:str):
    url = f'https://api.adviceslip.com/advice/search/{query}'

    return get_response(url)


if __name__ == '__main__':
    print(random_advice())
    print(advice_by_id(123))
    print(search_advice('studying'))


