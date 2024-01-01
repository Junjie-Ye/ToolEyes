
import requests

# This api only allows for a 21-day free trial.(Partial support for Chinese.)


def get_response(url, **kargs):
    response = requests.get(url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = 'http://api.weatherapi.com/v1'


def current_weather(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/current.json?key={api_key}&q={q}&lang={lang}'
    # print(url)
    return get_response(url)


def forecast(q: str, days: int = 1, api_key: str = '', lang: str = 'en', dt: str = None, unixdt: str = None, alerts: bool = False, aqi: bool = False, tp: bool = False, hour: int = None):
    days = int(days)
    if days < 1:
        days = 1
    elif days > 14:
        days = 14
    url = BASE_URL + \
        f'/forecast.json?key={api_key}&q={q}&lang={lang}&days={days}'
    # not the same time
    if dt != None:
        url += f"&dt={dt}"
    elif unixdt != None:
        url += f"&unixdt={unixdt}"
    if alerts == True:
        url += f"&alerts=yes"
    else:
        url += f"&alerts=no"
    if aqi == True:
        url += f"&aqi=yes"
    else:
        url += f"&aqi=no"
    if tp == True:
        url += f"&tp=15"
    if hour != None:
        url += f"&hour={hour}"
    # print(url)
    return get_response(url)


def history(q: str, dt: str, api_key: str = '', lang: str = 'en', unixdt: str = None, end_dt: str = None, unixend_dt: str = None, tp: bool = False, hour: int = None):
    url = BASE_URL+f'/history.json?key={api_key}&q={q}&lang={lang}'
    url += f"&dt={dt}"
    if unixdt != None:
        url += f"&unixdt={unixdt}"
    # only pass one of the end_dt
    if end_dt != None:
        url += f"&end_dt={end_dt}"
    elif unixend_dt != None:
        url += f"&unixend_dt={unixend_dt}"
    if hour != None:
        url += f"&hour={hour}"
    if tp == True:
        url += f"&tp=15"
    return get_response(url)


def marine(q: str, api_key: str = '', lang: str = 'en', tides: bool = False):
    url = BASE_URL+f'/marine.json?key={api_key}&q={q}&lang={lang}'
    if tides == True:
        url += f"&tides=yes"
    else:
        url += f"&tides=no"
    return get_response(url)


def future(q: str, dt: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/future.json?key={api_key}&q={q}&lang={lang}&dt={dt}'
    print(url)
    return get_response(url)


def search(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/search.json?key={api_key}&q={q}&lang={lang}'
    print(url)
    return get_response(url)


def ip_lookup(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/ip.json?key={api_key}&q={q}&lang={lang}'
    print(url)
    return get_response(url)


def astronomy_info(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/astronomy.json?key={api_key}&q={q}&lang={lang}'
    # print(url)
    return get_response(url)


def time_zone(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/timezone.json?key={api_key}&q={q}&lang={lang}'
    # print(url)
    return get_response(url)


def sports(q: str, api_key: str = '', lang: str = 'en'):
    url = BASE_URL+f'/sports.json?key={api_key}&q={q}&lang={lang}'
    # print(url)
    return get_response(url)


if __name__ == '__main__':
    print(current_weather(q="Shanghai"))
    # print(forecast(q="Shanghai",days=2,alerts=True))
    # print(history(q="Shanghai",dt='2023-08-10'))
    # print(marine(q="Shanghai"))
    # print(search(q="Shan",lang='zh'))
    # print(time_zone(q="Shanghai",lang='zh'))
    # print(ip_lookup(q='203.156.78.215'))
    # print(sports(q="London",lang='yue'))
    pass
