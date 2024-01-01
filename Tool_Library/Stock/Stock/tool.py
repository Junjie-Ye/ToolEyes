import requests
import json
from datetime import date, datetime, timedelta


def options_data(ticker: str, key: str = '',
                 Proxy_Secret: str = 'a755b180-f5a9-11e9-9f69-7bf51e845926'):
    ticker = ticker.lower()
    url = "https://stock-and-options-trading-data-provider.p.rapidapi.com/options/"+ticker
    headers = {
        "X-RapidAPI-Proxy-Secret": Proxy_Secret,
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "stock-and-options-trading-data-provider.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        return data["stock"]
    except:
        return response.text


BASE_URL = 'https://www.alphavantage.co/query?'


def get_json_data(function, symbol, interval='5min', adjusted='true', outputsize='compact', datatype='json',
                  key: str = ''):
    url = BASE_URL + 'function=' + function + \
        '&symbol=' + symbol + '&apikey=' + key
    r = requests.get(url)
    data = json.loads(r.text)
    return data


def get_today_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def add_date(date: str, days: int):
    date = datetime.strptime(date, "%Y-%m-%d")
    new_date = date + timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")


def get_daily_prices(symbol: str, date: str = '', key: str = ''):
    if "," in symbol:
        symbol, date = symbol.split(",")
    if date.strip() == "":
        return "Please specify a date and try again. You can you get_today_date to up-to-date time information."
    data = get_json_data('TIME_SERIES_DAILY', symbol, key)
    open_price = 'unknown'
    close_price = 'unknown'
    high_price = 'unknown'
    low_price = 'unknown'
    final_time = 'unknown'
    try:
        time_series = data["Time Series (Daily)"]
        for timestamp, daily_data in time_series.items():
            if timestamp == date:
                final_time = timestamp
                open_price = daily_data["1. open"]
                high_price = daily_data["2. high"]
                low_price = daily_data["3. low"]
                close_price = daily_data["4. close"]
                break
            elif timestamp < date:
                final_time = timestamp
                open_price = time_series[timestamp]["1. open"]
                high_price = time_series[timestamp]["2. high"]
                low_price = time_series[timestamp]["3. low"]
                close_price = time_series[timestamp]["4. close"]
                break
        return {'open': open_price, 'close': close_price, 'high': high_price, 'low': low_price, 'symbol': symbol, 'date': final_time}
    except:
        return data


def get_open_info(region: str, key: str = ''):
    url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=' + key
    r = requests.get(url)
    data = json.loads(r.text)
    for item in data['markets']:
        if item['region'] == region:
            return item['current_status']
    return ' not found'


def get_exchange_rate(from_currency: str, to_currency: str, key: str = ''):
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + \
        from_currency + '&to_currency=' + to_currency + '&apikey=' + key
    r = requests.get(url)
    data = json.loads(r.text)
    try:
        rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return rate
    except:
        return 'Invalid API call. Currency codes might be invalid.'


if __name__ == '__main__':
    # print(options_data('aapl'))
    # print(get_today_date())
    # print(add_date('2023-02-19', 100))
    print(get_daily_prices('600104.SHH', '2023-08-09'))
    # print(get_open_info('Mainland China'))
    # print(get_exchange_rate('USD','CNY'))
