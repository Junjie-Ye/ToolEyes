import requests
import json
import csv
import regex

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


def normalize_param_for_interval(string: str, l: list):
    for i in l:
        if is_similar_substring(i, string, 2):
            return i


commodity_list = [
    ['Crude Oil WIT', 'WTI'],
    ['Crude Oil Brent', 'BRENT'],
    ['Natural Gas', 'NATURAL_GAS'],
    ['Copper', 'COPPER'],
    ['Aluminum', 'ALUMINUM'],
    ['Wheat', 'WHEAT'],
    ['Corn', 'CORN'],
    ['Cotton', 'COTTON'],
    ['Sugar', 'SUGAR'],
    ['Coffee', 'COFFEE']
]


def levenshtein_distance(s, t):
    m = len(s)
    n = len(t)
    d = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(1, m + 1):
        d[i][0] = i

    for j in range(1, n + 1):
        d[0][j] = j

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # deletion
                          d[i][j - 1] + 1,      # insertion
                          d[i - 1][j - 1] + cost)  # substitution
    return d[m][n]


def get_commodity_price(
    apikey: str = default_apikey,
    interval: str = 'monthly',
    commodity: str = '',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(
        interval, ['daily', 'weekly', 'monthly'])

    macro = ''
    for l in commodity_list:
        if commodity.lower() in l[0].lower():
            macro = l[1]
    if macro == '':
        similarity_list = [[levenshtein_distance(
            l[0], commodity), l[1]] for l in commodity_list]
        min = similarity_list[0]
        for l in similarity_list:
            if l[0] < min[0]:
                min = l
        macro = min[1]

    return get_response(
        url=url,
        apikey=apikey,
        function=macro,
        interval=interval,
    )


def get_global_price_index_of_all_commodities(
    apikey: str = default_apikey,
    interval: str = 'monthly',
):
    url = 'https://www.alphavantage.co/query'
    interval = normalize_param_for_interval(
        interval, ['monthly', 'quarterly', 'annual'])
    return get_response(
        url=url,
        apikey=apikey,
        function='ALL_COMMODITIES',
        interval=interval,
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


if __name__ == '__main__':
    # Tests for helper functions
    # print(normalize_param_for_interval('day'))

    # pretty_print(get_commodity_price(interval='month',commodity='123'))
    pretty_print(get_global_price_index_of_all_commodities(interval='quarter'))
    # with open('text.txt','w') as f:
    #     f.write(json.dumps(get_global_price_index_of_all_commodities(interval='quarter'),indent=4))
