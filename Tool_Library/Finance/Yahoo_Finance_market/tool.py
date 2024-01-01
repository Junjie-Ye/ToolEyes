import requests
import json
import csv
import regex
import datetime
from dateutil.parser import parse
import time

doc_url = 'https://rapidapi.com/apidojo/api/yahoo-finance1/'
base_url = 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/screeners'
default_apikey = ''

region_list = ['US', 'BR', 'AU', 'CA', 'FR',
               'DE', 'HK', 'IN', 'IT', 'ES', 'GB', 'SG']


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


def dateparser(string: str):
    return parse(string).strftime('%Y-%m-%d')


def is_similar_substring(sub: str, sup: str, tolerance: int = 1):
    pattern_str = f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str, sup) != None


def normalize_param_for_interval(string: str, l: list):
    for i in l:
        if is_similar_substring(i, string, 2):
            return i


def normalize_param_for_region(string: str):
    try:
        region = normalize_param_for_interval(region, region_list, 0)
    except:
        return {'Error': "Region symbol given is not included in region_list = ['US','BR','AU','CA','FR','DE','HK','IN','IT','ES','GB','SG']"}
    return region


def get_autocomplete(
    apikey: str = default_apikey,
    q: str = '',
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "region": region,
        "q": q,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_quotes(
    apikey: str = default_apikey,
    symbols: str = '',
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "region": region,
        "symbols": symbols,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_summary(
    apikey: str = default_apikey,
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-summary"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "region": region,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_tickers_by_quote_type(
    apikey: str = default_apikey,
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-tickers-by-quote-type"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "region": region,
        'lang': 'en-US'
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_spark(
    apikey: str = default_apikey,
    symbols: str = '',
    interval: str = '1m',
    range: str = '1d'
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-spark"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    interval = normalize_param_for_interval(
        interval, ['5m', '15m', '1d', '1wk', '1mo'])
    range = normalize_param_for_interval(
        range, ['1d', '5d', '3mo', '6mo', '1y', '5y', 'max'])
    querystring = {
        "symbols": symbols,
        'interval': interval,
        'range': range
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_earnings(
    apikey: str = default_apikey,
    region: str = 'US',
    start_date: str = '',
    end_date: str = '',
    size: int = 10,
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-earnings"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    try:
        start_date = int(datetime.datetime.timestamp(parse(start_date))*1000)
        end_date = int(datetime.datetime.timestamp(parse(end_date))*1000)
    except:
        return {'Error': 'Date parser error.'}
    querystring = {
        'region': region,
        "startDate": start_date,
        'endDate': end_date,
        'size': size
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_trending_tickers(
    apikey: str = default_apikey,
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        'region': region,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_popular_watchlists(
    apikey: str = default_apikey,
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-popular-watchlists"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


def file_print(t):
    with open('text.txt', 'w') as f:
        f.write(json.dumps(t, indent=4))


if __name__ == '__main__':
    # pretty_print(get_autocomplete(q='tesla'))
    # pretty_print(get_quotes(symbols='AMD,IBM'))
    # file_print(get_summary(region='HK'))
    # file_print(get_tickers_by_quote_type(region='HK'))
    # file_print(get_spark(symbols='AMZN,AAPL,WDC,REYN,AZN,YM=F',interval='1m',range='1d'))
    file_print(get_earnings(start_date='2022-01-01', end_date='20230101'))
    # file_print(get_trending_tickers())
    # file_print(get_popular_watchlists())
