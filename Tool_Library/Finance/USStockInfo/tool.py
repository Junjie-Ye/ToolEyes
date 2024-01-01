import requests
import datetime
from dateutil.parser import parse
import json
import csv

doc_url = 'https://www.alphavantage.co/documentation/#symbolsearch'
base_url = 'https://api.1forge.com'
default_apikey = ''
# Standard API call frequency is 5 calls per minute and 100 calls per day.


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    kargs = remove_empty_value_for_dict(kargs)
    # print(kargs)
    # print(response.url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_company_overview(
    symbol: str,
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='OVERVIEW',
    )


def get_income_statement(
    symbol: str,
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='INCOME_STATEMENT',
    )


def get_balance_sheet(
    symbol: str,
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='BALANCE_SHEET',
    )


def get_cash_flow(
    symbol: str,
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='CASH_FLOW',
    )


def get_earnings(
    symbol: str,
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='EARNINGS',
    )


def dateparser(string: str):
    return parse(string).strftime('%Y-%m-%d')


def csv_string_to_json(string: str):
    lines = string.splitlines()
    new_lines = [line.strip() for line in lines if line]
    jsonArray = []
    new_string = '\n'.join(new_lines)
    reader = csv.DictReader(new_lines)
    for row in reader:
        jsonArray.append(row)
    return jsonArray


def get_listing_and_delisting_status(
    allow_delisted: bool = False,
    date: str = '',
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    if allow_delisted:
        state = 'delisted'
    else:
        state = 'active'
    try:
        date = dateparser(date)
    except:
        date = ''

    return csv_string_to_json(get_response(
        url=url,
        apikey=apikey,
        state=state,
        date=date,
        function='LISTING_STATUS',
    ))


def get_earnings_calender(
    symbol: str,
    horizon: int = 3,
    apikey: str = default_apikey
):
    horizon = int(horizon)
    url = 'https://www.alphavantage.co/query'
    if horizon <= 3:
        horizon = 3
    elif horizon <= 6:
        horizon = 6
    else:
        horizon = 12
    horizon = str(horizon)+'month'
    response_text = get_response(
        url=url,
        apikey=apikey,
        symbol=symbol,
        function='EARNINGS_CALENDAR',
        horizon=horizon,
    )
    # API returning csv string
    return csv_string_to_json(response_text)


def get_ipo_calendar(
    apikey: str = default_apikey
):
    url = 'https://www.alphavantage.co/query'
    return csv_string_to_json(get_response(
        url=url,
        apikey=apikey,
        function='IPO_CALENDAR',
    ))


if __name__ == '__main__':
    # print(get_company_overview(symbol='BILI'))
    # print(get_income_statement(symbol='BILI'))
    # print(get_balance_sheet(symbol='BILI'))
    # print(get_cash_flow(symbol='BILI'))
    # print(get_earnings(symbol='BILI'))
    print(json.dumps(get_listing_and_delisting_status(
        date='12dff'), indent=4))  # catch error
    # print(get_earnings_calender(horizon=6,symbol='BILI'))
    # print(get_ipo_calendar())

    # Tests for helper function
    # print(
    #     json.dumps(
    #     csv_string_to_json(
    #     '''
    #     a,b,c
    #     1,2,3
    #     2,3,4
    #     3,4,5
    #     '''
    #     ),indent=4
    # ))
