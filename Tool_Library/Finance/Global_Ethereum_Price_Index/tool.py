import requests
import json
import csv
import regex

doc_url = 'https://rapidapi.com/blockchain-data-ltd-blockchain-data-ltd-default/api/global-ethereum-price-index-gex'
base_url = 'https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices'
default_apikey = ''
# slow response warning


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_custom_ticker(
    apikey: str = default_apikey,
    exchanges: str = '',
    if_include: bool = True,
    symbol: str = ''
):
    url = f"https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices/ticker/custom/{'include' if if_include else 'exclude'}/{symbol}"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com"
    }
    querystring = {"exchanges": exchanges}
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )

# eg: input='ETHUSD', output=infos of it


def get_ticker_per_symbol(
    apikey: str = default_apikey,
    if_global: bool = True,
    symbol: str = ''
):
    url = f"https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices/{'global' if if_global else 'local'}/ticker/{symbol}"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )

# crypto='ETH', fiats='USD,EUR'. output=infos of 'ETHUSD'&'ETHEUR'


def get_short_ticker(
    apikey: str = default_apikey,
    if_global: bool = True,
    crypto: str = 'ETH',
    fiats: str = '',
):
    url = f"https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices/{'global' if if_global else 'local'}/ticker/short"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com"
    }
    querystring = {"crypto": crypto, "fiats": fiats}
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_ticker_changes(
    apikey: str = default_apikey,
    if_global: bool = True,
    symbol: str = ''
):
    url = f"https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices/{'global' if if_global else 'local'}/ticker/{symbol}/changes"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def get_all_ticker_data(
    apikey: str = default_apikey,
    if_global: bool = True,
    crypto: str = 'ETH',
    fiats: str = '',
):
    url = f"https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices/{'global' if if_global else 'local'}/ticker/all"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com"
    }
    querystring = {"crypto": crypto, "fiats": fiats}
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


def file_print(t):
    with open('text.txt', 'w') as f:
        f.write(json.dumps(t, indent=4))


if __name__ == '__main__':
    # pretty_print(get_custom_ticker(exchanges='bitfinex,bitstamp',if_include=True, symbol='ETHUSD'))
    # pretty_print(get_ticker_per_symbol(if_global=True, symbol='ETHUSD'))
    file_print(get_short_ticker(if_global=True, crypto='ETH', fiats='USD,EUR'))
    # pretty_print(get_ticker_changes(if_global=True, symbol='ETHUSD'))
    # file_print(get_all_ticker_data(if_global=True, crypto='ETH',fiats='USD,EUR'))
