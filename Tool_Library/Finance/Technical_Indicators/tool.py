import requests
import datetime
from dateutil.parser import parse
import json
import csv
import regex

doc_url = 'https://www.alphavantage.co/documentation/#symbolsearch'
base_url = 'https://api.1forge.com'
default_apikey = ''
# Standard API call frequency is 5 calls per minute and 100 calls per day.


def remove_empty_value_for_dict(d:dict):
    temp=[d]
    res = list(filter(
    None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]

def get_response(url, **kargs):
    response = requests.get(url, kargs) 
    kargs=remove_empty_value_for_dict(kargs)
    # print(kargs)
    # print(response.url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation

def is_similar_substring(sub:str,sup:str,tolerance:int=1):
    pattern_str=f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str,sup)!=None

def normalize_param_for_interval(string:str,l:list,tolerance:int=2):
    for i in l:
        if is_similar_substring(i,string,tolerance):
            return i
        
        
from .symbols import *


def get_technical_indicator_of_ticker(
    apikey: str = default_apikey,
    indicator_symbol:str='',
    interval:str='hourly',
    symbol:str='',
    series_type:str='close',
):
    url = 'https://www.alphavantage.co/query'
    indicator_symbol=indicator_symbol.upper()
    if indicator_symbol not in indicator_symbols:
        return ({
            'Error':'Please check indicator symbol input.'
        })
    interval=normalize_param_for_interval(interval,['hourly','daily','weekly','monthly'])
    series_type=normalize_param_for_interval(series_type,['close','open','high','low'],1)
    return get_response(
        url=url,
        apikey=apikey,
        function=indicator_symbol,
        interval=interval,
        symbol=symbol,
        time_period=60,
        series_type=series_type
    )

def get_all_technical_indicators_available():
    dict={}
    for i in range(len(indicator_symbols)):
        dict[indicator_symbols[i]]=indicator_description[i]
    return dict

def get_technical_indicator_description(
    indicator_symbol:str=''
):
    return({
        'symbol':indicator_symbol,
        'description':get_all_technical_indicators_available()[indicator_symbol]
    })

def pretty_print(t):
    print(json.dumps(t,indent=4))
    
if __name__ == '__main__':
    # for i in indicator_symbol:
    #     for j in indicator_symbol:
    #         if i!=j and (i in j or j in i):
    #             print(i,j)
    
    # print(len(indicator_symbols),len(indicator_description))
    # pretty_print(get_all_technical_indicators_available())
    pretty_print(get_technical_indicator_description('SMA'))
    
    # pretty_print(get_technical_indicator_of_ticker(indicator_symbol='SMA',interval='daily',symbol='IBM'))

    