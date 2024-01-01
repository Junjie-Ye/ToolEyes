import requests


def get_response(url, kv_dict=None):
    response = requests.get(url, params=kv_dict)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def generate_music():
    url = "https://binaryjazz.us/wp-json/genrenator/v1/genre/"
    return get_response(url)


def generate_story():
    url = "https://binaryjazz.us/wp-json/genrenator/v1/story/"
    return get_response(url)


def search_itunes(term: str, country: str, media: str = None, entity: str = None, attribute: str = None, limit: int = None, lang: str = None, explicit: str = None):
    url = "https://itunes.apple.com/search?{}"
    kv_dict = []

    kv_dict.append(('term', term))
    kv_dict.append(('country', country))
    kv_dict.append(('media', media))
    kv_dict.append(('attribute', attribute))
    kv_dict.append(('entity', entity))
    kv_dict.append(('limit', limit))
    kv_dict.append(('lang', lang))
    kv_dict.append(('explicit', explicit))
    return get_response(url, kv_dict)


if __name__ == '__main__':
    pass
    # print(generate_music())
    # print(generate_story())
    # print(search_itunes(term="Bruno",country='US',lang="ja_jp",limit=25))
