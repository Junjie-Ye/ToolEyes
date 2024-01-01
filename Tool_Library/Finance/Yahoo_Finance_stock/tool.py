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


def get_summary(
    apikey: str = default_apikey,
    symbol: str = '',
    region: str = 'US',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "region": region,
        "symbol": symbol,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_recommendations(
    apikey: str = default_apikey,
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-recommendations"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    querystring = {
        "symbol": symbol,
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_upgrades_downgrades(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-upgrades-downgrades"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_analysis(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_statistics(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v4/get-statistics"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_historical_data(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_profile(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-profile"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_financials(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_cash_flow(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-cash-flow"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_balance_sheet(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-balance-sheet"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_options(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-options"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_holders(
    apikey: str = default_apikey,
    region: str = 'US',
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-holders"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    region = normalize_param_for_region(region)
    querystring = {
        "symbol": symbol,
        'region': region,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_holdings(
    apikey: str = default_apikey,
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-holdings"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    querystring = {
        "symbol": symbol,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_insights(
    apikey: str = default_apikey,
    symbol: str = '',
):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-insights"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    querystring = {
        "symbol": symbol,
        'lang': 'en-US',
    }
    querystring = remove_empty_value_for_dict(querystring)
    return get_response(
        url=url,
        headers=headers,
        params=querystring
    )


def get_insider_transactions(
    apikey: str = default_apikey,
    symbol: str = '',
    region: str = 'US',
):
    region = normalize_param_for_region(region)
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-insider-transactions"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    querystring = {
        "symbol": symbol,
        'lang': 'en-US',
        'region': region
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
    # pretty_print(get_summary(symbol='AMRN'))
    file_print(get_recommendations(symbol='AMRN'))
    # file_print(get_upgrades_downgrades(symbol='AMRN'))
    # file_print(get_analysis(symbol='AMRN'))
    # file_print(get_statistics(symbol='AMRN'))
    # file_print(get_historical_data(symbol='AMRN'))
    # file_print(get_profile(symbol='AMRN'))
    # file_print(get_financials(symbol='AMRN'))
    # file_print(get_cash_flow(symbol='AMRN'))
    # file_print(get_balance_sheet(symbol='AMRN'))
    # file_print(get_options(symbol='AMRN'))
    # file_print(get_holders(symbol='AMRN'))
    # file_print(get_holdings(symbol='VBIAX'))
    # file_print(get_insights(symbol='AMRN'))
    # file_print(get_insider_transactions(symbol='AMRN'))
    # file_print(get_insider_transactions(symbol='AMRN'))
