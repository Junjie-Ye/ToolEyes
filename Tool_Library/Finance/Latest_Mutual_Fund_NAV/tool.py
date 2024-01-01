import requests
import json
import csv
import regex
import datetime
from dateutil.parser import parse

doc_url = 'https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav'
base_url = 'https://latest-mutual-fund-nav.p.rapidapi.com'
default_apikey = ''
# slow response warning


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]


def get_response(url, headers, params={}):
    response = requests.get(url, headers=headers, params=params)
    # print(response.url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def dateparser(string: str):
    return parse(string).strftime('%d-%b-%Y')


def is_similar_substring(sub: str, sup: str, tolerance: int = 1):
    pattern_str = f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str, sup) != None


def normalize_param_for_interval(string: str, l: list, tolerance: int = 2):
    for i in l:
        if is_similar_substring(i.lower(), string.lower(), tolerance):
            return i


def fetch_latest_nav(
    apikey: str = default_apikey,
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchLatestNAV"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def fetch_historical_nav(
    apikey: str = default_apikey,
    date: str = '',
    SchemeName: str = '',
    SchemeType: str = '',
    MutualFundFamily: str = '',
    SchemeCategory: str = '',
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchHistoricalNAV"
    querystring = {
        "Date": dateparser(date),
        "SchemeName": SchemeName,
        "SchemeType": SchemeType,
        "MutualFundFamily": MutualFundFamily,
        "SchemeCategory": SchemeCategory,
    }
    querystring = remove_empty_value_for_dict(querystring)
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
        params=querystring,
    )


def fetch_all_scheme_types(
    apikey: str = default_apikey,
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchAllSchemeTypes"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def fetch_all_scheme_names(
    apikey: str = default_apikey,
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchAllSchemeNames"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def fetch_all_mutual_fund_families(
    apikey: str = default_apikey,
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchAllMutualFundFamilies"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    return get_response(
        url=url,
        headers=headers,
    )


def fetch_scheme_categories_by_scheme_type(
    apikey: str = default_apikey,
    scheme_type: str = 'All',
):
    url = f"https://latest-mutual-fund-nav.p.rapidapi.com/fetchAllMutualFundFamilies"
    headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "latest-mutual-fund-nav.p.rapidapi.com"
    }
    scheme_type = normalize_param_for_interval(scheme_type, [
                                               'All', 'Open Ended Schemes', 'Interval Fund Schemes', 'Close Ended Schemes'])
    querystring = {"SchemeType": scheme_type}
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
    # pretty_print(fetch_latest_nav())
    # file_print(fetch_historical_nav(date='2022-12-01'))
    pretty_print(fetch_all_scheme_types())
    # file_print(fetch_all_scheme_names())
    # file_print(fetch_all_mutual_fund_families())
    # pretty_print(fetch_scheme_categories_by_scheme_type(scheme_type='Open Ended Schemes'))
