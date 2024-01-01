import requests


def get_response(url: str, **kargs):
    try:
        response = requests.post(url, kargs)
    except:
        return {"error": "connection error."}

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


def get_categorization(txt: str, model: str = 'IAB_2.0_en', key: str = ''):
    url = 'https://api.meaningcloud.com/deepcategorization-1.0'
    return get_response(url=url, txt=txt, model=model, key=key)


def get_topics(txt: str, tt: str = 'a', key: str = ''):
    url = 'https://api.meaningcloud.com/topics-2.0'
    return get_response(url, txt=txt, tt=tt, key=key, lang='en')


def sentiment_analysis(txt: str, key: str = ''):
    url = 'https://api.meaningcloud.com/sentiment-2.1'
    return get_response(url, txt=txt, key=key, lang='en')


def linguistic_analysis(txt: str, key: str = ''):
    url = 'https://api.meaningcloud.com/parser-2.0'
    return get_response(url, txt=txt, key=key, lang='en')


def text_cluster(txt: str, key: str = ''):
    url = 'https://api.meaningcloud.com/clustering-1.1'
    return get_response(url, txt=txt, key=key, lang='en')


def summarization(txt: str, sentences: int = 1, key: str = ''):
    url = 'https://api.meaningcloud.com/summarization-1.0'
    return get_response(url, txt=txt, sentences=sentences, key=key, lang='en')


def document_structure(txt: str = None, txt_url: str = None, key: str = ''):
    url = 'https://api.meaningcloud.com/documentstructure-1.0'
    payload = {
        'key': key,
    }
    if txt is None:
        payload['url'] = txt_url
    else:
        payload['txt'] = txt

    try:
        response = requests.post(url, data=payload)
    except:
        return {"error": "connection error."}

    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


if __name__ == '__main__':
    # print(get_categorization("As the gentle waves caress the sandy beach and the sunlight pours down its warm rays, I feel a sense of tranquility and peace within. The beauty and harmony of nature make me forget the hustle and bustle of the city, allowing me to quietly listen to the birds' songs and feel the breath of the wind. In this serene corner, I find a sanctuary for my soul, a place of calmness and freedom away from the chaos. The picturesque scenery freezes time, enabling me to fully embrace the gifts of nature."))
    # print(get_topics("As the gentle waves caress the sandy beach and the sunlight pours down its warm rays, I feel a sense of tranquility and peace within. The beauty and harmony of nature make me forget the hustle and bustle of the city, allowing me to quietly listen to the birds' songs and feel the breath of the wind. In this serene corner, I find a sanctuary for my soul, a place of calmness and freedom away from the chaos. The picturesque scenery freezes time, enabling me to fully embrace the gifts of nature."))
    # print(sentiment_analysis("As the gentle waves caress the sandy beach and the sunlight pours down its warm rays, I feel a sense of tranquility and peace within. The beauty and harmony of nature make me forget the hustle and bustle of the city, allowing me to quietly listen to the birds' songs and feel the breath of the wind. In this serene corner, I find a sanctuary for my soul, a place of calmness and freedom away from the chaos. The picturesque scenery freezes time, enabling me to fully embrace the gifts of nature."))
    # print(linguistics_analysis("As the gentle waves caress the sandy beach and the sunlight pours down its warm rays, I feel a sense of tranquility and peace within. The beauty and harmony of nature make me forget the hustle and bustle of the city, allowing me to quietly listen to the birds' songs and feel the breath of the wind. In this serene corner, I find a sanctuary for my soul, a place of calmness and freedom away from the chaos. The picturesque scenery freezes time, enabling me to fully embrace the gifts of nature."))
    # print(text_cluster("He earns $200,000/yr and still has a mortgage on his house :(\nZara clothes will be the death of my credit card\nMy bank insisted I destroyed my credit card before I could get a mortgage\nI'm not paying the mortgage or credit card bills\nTell them you've never had a loan, you have no mortgage"))
    # print(summarization("As the gentle waves caress the sandy beach and the sunlight pours down its warm rays, I feel a sense of tranquility and peace within. The beauty and harmony of nature make me forget the hustle and bustle of the city, allowing me to quietly listen to the birds' songs and feel the breath of the wind. In this serene corner, I find a sanctuary for my soul, a place of calmness and freedom away from the chaos. The picturesque scenery freezes time, enabling me to fully embrace the gifts of nature."))
    # print(document_structure(txt_url=r"https://en.wikipedia.org/wiki/Margaret_Hamilton_(software_engineer)", ))
    pass
