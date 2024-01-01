import requests
import json
import csv
import regex
import datetime
from dateutil.parser import parse

doc_url = 'https://rapidapi.com/blockchain-data-ltd-blockchain-data-ltd-default/api/global-ethereum-price-index-gex'
base_url = 'https://bitcoinaverage-global-ethereum-index-v1.p.rapidapi.com/indices'
default_apikey = ''


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


def currency_converter(
    apikey: str = default_apikey,
    from_currency: str = '',
    to_currency: str = '',
    amount: int = 1,
):
    amount = int(amount)
    url = f"https://currency-converter5.p.rapidapi.com/currency/convert"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }
    amount = amount if amount >= 0 else -amount
    querystring = {
        "format": "json",
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "language": 'en',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def dateparser(string: str):
    return parse(string).strftime('%Y-%m-%d')


def historical_currency_data(
    apikey: str = default_apikey,
    from_currency: str = '',
    to_currency: str = '',
    amount: int = 1,
    date: str = '',
):
    amount = int(amount)
    url = f"https://currency-converter5.p.rapidapi.com/currency/convert"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }
    amount = amount if amount >= 0 else -amount
    date = dateparser(date)
    querystring = {
        "format": "json",
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "language": 'en',
        "date": date
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def available_currencies(
    apikey: str = default_apikey,
):
    url = f"https://currency-converter5.p.rapidapi.com/currency/convert"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }
    querystring = {
        "format": "json",
        "language": 'en',
    }
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
    # pretty_print(currency_converter(from_currency='USD',to_currency='CNY',amount=10))
    # pretty_print(historical_currency_data(from_currency='USD',to_currency='CNY',amount=10,date='20220101'))
    pretty_print(available_currencies())
