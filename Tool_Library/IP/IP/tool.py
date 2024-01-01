import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def ip_country(ip: str):
    url = 'https://api.country.is/{}'.format(ip)
    return get_response(url)


def ip_details(ip: str):
    url = 'http://ipwho.is/{}'.format(ip)
    return get_response(url)


def get_ip():
    url = 'https://api64.ipify.org?format=json'
    return get_response(url)


def ip_more(ip: str, api_key=''):
    url = 'https://ipinfo.io/{}?token={}'.format(ip, api_key)
    return get_response(url)


if __name__ == '__main__':
    ip = "9.9.9.9"
    # print(ip_country(ip))
    # print(ip_details(ip))
    # print(get_ip())
    # print(ip_more(ip))
    print(ip_details(ip="2001:470:f939:f80f::1"))
