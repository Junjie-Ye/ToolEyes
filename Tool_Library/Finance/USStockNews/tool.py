import requests
import regex
import datetime
from dateutil.parser import parse

doc_url = 'https://www.alphavantage.co/documentation/#symbolsearch'
base_url = 'https://api.1forge.com'
# default_apikey = ''
# Standard API call frequency is 5 calls per minute and 100 calls per day.

topics_list = [
    "blockchain",
    "earnings",
    "ipo",
    "mergers_and_acquisitions",
    "financial_markets",
    "economy_fiscal",
    "economy_monetary",
    "economy_macro",
    "energy_transportation",
    "finance",
    "life_sciences",
    "manufacturing",
    "real_estate",
    "retail_wholesale",
    "technology"
]


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    kargs = remove_empty_value_for_dict(kargs)
    # print(kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def dateparser(string: str):
    return parse(string).strftime('%Y%m%dT%H%M')


def is_similar_substring(sub: str, sup: str, tolerance: int = 1):
    pattern_str = f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str, sup) != None


def recognizing_tolerance(len: int):
    if len <= 5:
        return 0
    elif len <= 10:
        return 1
    else:
        return 3


def refractor_parameter_for_topics(string: str):
    temp_topics_list = []
    for i in topics_list:
        temp_tolerance = recognizing_tolerance(len(i))
        if (is_similar_substring(i, string, temp_tolerance)):
            temp_topics_list.append(i)
    return ','.join(temp_topics_list)


def get_market_news_and_sentiment(
    tickers: str = '',
    topics: str = '',
    time_from: str = '',
    time_to: str = '',
    limit: int = 50,   # Probably not functioning
    apikey: str = ''
):
    url = 'https://www.alphavantage.co/query'
    topics = refractor_parameter_for_topics(topics)
    try:
        time_from = dateparser(time_from)
    except:
        time_from = ''
    try:
        time_to = dateparser(time_to)
    except:
        time_to = ''
    return get_response(
        url=url,
        apikey=apikey,
        function='NEWS_SENTIMENT',
        tickers=tickers,
        topics=topics,
        time_from=time_from,
        time_to=time_to,
        limit=limit
    )


def get_special_tickers(
    apikey: str = ''
):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        apikey=apikey,
        function='TOP_GAINERS_LOSERS',
    )


if __name__ == '__main__':
    # Tests for helpers
    # print(regex.search(r"(?:blockchain){e<=1}", "favor in blockchain"))
    # print(is_similar_substring(sub='blockchain',sup='favor in blockchain'))
    # print(refractor_parameter_for_topics("ipo,earnings and mergers_and_acuisitions"))
    # print(remove_empty_value_for_dict({'a':12,'b':None}))
    # print(get_market_news_and_sentiment())

    # file1=get_market_news_and_sentiment(
    #     tickers='BILI',topics='ipo',time_from='20230501',limit=1000
    # )
    # import json
    # with open('./text.txt','w') as f:
    #     f.write(json.dumps(file1,indent=4))

    print(get_market_news_and_sentiment(
        tickers='BILI', topics='ipo', time_from='20230501', limit=1000
    ))
    print(get_special_tickers())
