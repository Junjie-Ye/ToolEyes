import requests

doc_url = 'https://www.alphavantage.co/documentation/#symbolsearch'
base_url = 'https://api.1forge.com'
# default_apikey = ''


def get_response(url, **kargs):
    # print(kargs)
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_stock_time_series_intraday(symbol: str, interval: int = 30, fulldata: bool = False, apikey: str = ''
                                   ):
    interval = int(interval)
    url = 'https://www.alphavantage.co/query'
    if interval >= 60:
        intervalstr = '60min'
    elif interval >= 30:
        intervalstr = '30min'
    elif interval >= 15:
        intervalstr = '15min'
    elif interval >= 5:
        intervalstr = '5min'
    else:
        intervalstr = '1min'

    if fulldata:
        outputsizestr = 'full'
    else:
        outputsizestr = 'compact'
    return get_response(
        url=url,
        symbol=symbol,
        function='TIME_SERIES_INTRADAY',
        interval=intervalstr,
        apikey=apikey,
        outputsize=outputsizestr
    )


def get_stock_time_series_daily(symbol: str, fulldata: bool = False, apikey: str = ''
                                ):
    url = 'https://www.alphavantage.co/query'
    if fulldata:
        outputsizestr = 'full'
    else:
        outputsizestr = 'compact'
    return get_response(
        url=url,
        symbol=symbol,
        function='TIME_SERIES_DAILY',
        apikey=apikey,
        outputsize=outputsizestr
    )


def get_stock_time_series_weekly(symbol: str, apikey: str = ''
                                 ):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        symbol=symbol,
        function='TIME_SERIES_WEEKLY',
        apikey=apikey,
    )


def get_stock_time_series_monthly(symbol: str, apikey: str = ''
                                  ):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        symbol=symbol,
        function='TIME_SERIES_MONTHLY',
        apikey=apikey,
    )


def get_stock_quote_endpoint(symbol: str, apikey: str = ''
                             ):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        symbol=symbol,
        function='GLOBAL_QUOTE',
        apikey=apikey,
    )


def get_stock_symbol_search_endpoint(keywords: str, apikey: str = ''
                                     ):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        keywords=keywords,
        function='SYMBOL_SEARCH',
        apikey=apikey,
    )


def get_global_market_open_and_close_status(apikey: str = ''
                                            ):
    url = 'https://www.alphavantage.co/query'
    return get_response(
        url=url,
        function='MARKET_STATUS',
        apikey=apikey,
    )


if __name__ == '__main__':
    # print(get_stock_time_series_intraday(symbol='IBM',fulldata=True))
    # print(get_stock_time_series_daily(symbol='SOHU'))
    # print(get_stock_time_series_weekly(symbol='BILI'))
    # print(get_stock_time_series_monthly(symbol='BILI'))
    # print(get_stock_quote_endpoint(symbol='BILI'))
    # print(get_stock_symbol_search_endpoint(keywords='bili'))
    print(get_global_market_open_and_close_status())
