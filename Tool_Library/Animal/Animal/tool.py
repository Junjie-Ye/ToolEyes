import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def cat_breed(limit: int):
    url = "https://catfact.ninja/breeds"

    return get_response(url, limit=limit)


def cat_facts(max_length: int, limit: int = 1):
    url = "https://catfact.ninja/facts"

    return get_response(url, max_length=max_length, limit=limit)


def dog_breed():
    url = "https://dog.ceo/api/breeds/list/all"

    return get_response(url)


def dog_facts(number:int=1):
    url = 'http://dog-api.kinduff.com/api/facts'

    return get_response(url, number=number)


def random_dog_image(limit: int = 1):
    url = f'https://dog.ceo/api/breeds/image/random/{limit}'

    return get_response(url)


def all_dog_image_by_breed(breed: str):
    url = f'https://dog.ceo/api/breed/{breed}/images'

    return get_response(url)


def random_dog_image_by_breed(breed: str, limit: int = 1):
    url = f'https://dog.ceo/api/breed/{breed}/images/random/{limit}'

    return get_response(url)


def dog_sub_breed(breed: str):
    url = f'https://dog.ceo/api/breed/{breed}/list'

    return get_response(url)


def all_dog_image_by_sub_breed(breed: str, subbreed: str):
    url = f'https://dog.ceo/api/breed/{breed}/{subbreed}/images'

    return get_response(url)


def random_dog_image_by_sub_breed(breed: str, subbreed: str, limit: int = 1):
    url = f'https://dog.ceo/api/breed/{breed}/{subbreed}/images/random/{limit}'

    return get_response(url)


if __name__ == '__main__':
    # print(cat_breed(2))
    # print(cat_fact(100))
    # print(cat_facts(100, 3))
    print(dog_breed())
    print(dog_facts(2))
