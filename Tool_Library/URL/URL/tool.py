import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def shorten_url(long_url: str):
    url = 'https://cleanuri.com/api/v1/shorten'

    data = {'url': long_url}
    response = requests.post(url, data=data)

    short_url = response.text
    return short_url


def paper_rank(domains: list[str], api_key=''):
    url = 'https://openpagerank.com/api/v1.0/getPageRank'
    query = {
        'domains[]': domains
    }
    headers = {'API-OPR': api_key}

    response = requests.get(url, params=query, headers=headers)
    output = response.json()
    return output


if __name__ == '__main__':
    pass
    # print(shorten_url('https://www.google.com/'))
    # domains = ['google.com', 'facebook.com', 'youtube.com']
    # print(paper_rank(domains))
