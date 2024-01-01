import requests
import json
import csv
import regex
import re

doc_url = 'https://www.alphavantage.co/documentation/#symbolsearch'
base_url = 'https://api.1forge.com'
default_apikey = ''
# Standard API call frequency is 5 calls per minute and 100 calls per day.
free_api_terms_of_use = 'https://fred.stlouisfed.org/docs/api/terms_of_use.html'


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


def csv_string_to_json(string: str):
    lines = string.splitlines()
    new_lines = [line.strip() for line in lines if line]
    jsonArray = []
    new_string = '\n'.join(new_lines)
    reader = csv.DictReader(new_lines)
    for row in reader:
        jsonArray.append(row)
    return jsonArray


def is_similar_substring(sub: str, sup: str, tolerance: int = 1):
    pattern_str = f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str, sup) != None


def normalize_param_for_interval(string: str, l: list, tolerance: int = 2):
    for i in l:
        if is_similar_substring(i, string, tolerance):
            return i


def get_us_real_gdp(
    apikey: str = default_apikey,
    interval: str = 'annual',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(interval, ['annual', 'quarterly'])
    return get_response(
        url=url,
        apikey=apikey,
        function='REAL_GDP',
        interval=interval,
    )


def get_us_real_gdp_per_capita(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='REAL_GDP_PER_CAPITA',
    )


def normalize_param_for_maturity(string: str):
    if 'month' in string:
        return '3month'
    pattern = r'\d+'
    result = re.findall(pattern=pattern, string=string)
    num = int(result[0])
    num_list = [2, 5, 7, 10, 30]
    for i in num_list:
        if num <= i:
            return str(i)+'year'
    return '30year'


def get_us_treasury_yield(
    apikey: str = default_apikey,
    interval: str = 'monthly',
    maturity: str = '10year',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(
        interval, ['monthly', 'daily', 'weekly'])
    maturity = normalize_param_for_maturity(maturity)

    return get_response(
        url=url,
        apikey=apikey,
        interval=interval,
        function='TREASURY_YIELD',
        maturity=maturity,
    )


def get_us_federal_funds_rate(
    apikey: str = default_apikey,
    interval: str = 'monthly',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(
        interval, ['monthly', 'daily', 'weekly'])
    return get_response(
        url=url,
        apikey=apikey,
        interval=interval,
        function='FEDERAL_FUNDS_RATE',
    )


def get_us_cpi(
    apikey: str = default_apikey,
    interval: str = 'monthly',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(
        interval, ['monthly', 'semiannual',])
    return get_response(
        url=url,
        apikey=apikey,
        interval=interval,
        function='CPI',
    )


def get_us_inflation(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='INFLATION',
    )


def get_us_retail_sales(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='RETAIL_SALES',
    )


def get_us_durables(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='DURABLES',
    )


def get_us_unemployment(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='UNEMPLOYMENT',
    )


def get_us_nonfarm_payroll(
    apikey: str = default_apikey,
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='NONFARM_PAYROLL',
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


if __name__ == '__main__':
    # Tests for helper functions
    # normalize_param_for_maturity('12year')

    # pretty_print(get_us_real_gdp())
    # pretty_print(get_us_real_gdp_per_capita())
    # pretty_print(get_us_treasury_yield(maturity='25years'))
    # pretty_print(get_us_federal_funds_rate())
    # pretty_print(get_us_cpi())
    # pretty_print(get_us_inflation())
    # pretty_print(get_us_retail_sales())
    # pretty_print(get_us_durables())
    # pretty_print(get_us_unemployment())
    # pretty_print(get_us_nonfarm_payroll())

    with open('text.txt', 'w') as f:
        f.write(json.dumps(get_us_nonfarm_payroll(), indent=4))
