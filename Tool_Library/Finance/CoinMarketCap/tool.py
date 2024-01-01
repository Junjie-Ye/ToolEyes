import requests
import json
import csv
import regex
import os
import datetime
from dateutil.parser import parse

doc_url = 'https://coinmarketcap.com/api/documentation/v1/#section/Introduction'
base_url = 'pro-api.coinmarketcap.com'
default_apikey = ''

# Monthly credit limit: 10,000 (hard cap)
# Historical data access: No historical data
# Daily Historical data access: No historical data
# API call rate limit: 30 requests a minute

'''
只有以下功能是Basic免费方案可用的
cryptocurrency
	Categories
	Category
	CoinMarketCap ID Map
	Metadata v2
	Listings Latest
	Quotes Latest v2
fiat
	CoinMarketCap ID Map
exchange
	Exchange Assets
	Metadata
	CoinMarketCap ID Map
global-metrics
	Quotes Latest
tools
	Price Conversion v2
'''


def render_url(endpoint, params):
    url = f"https://pro-api.coinmarketcap.com{endpoint}"
    if not params:
        return url
    paramstr = '?'
    item_list = list(params.items())
    for i in range(len(item_list)):
        paramstr = paramstr+str(item_list[i][0])+'='+str(item_list[i][1])
        if i != len(item_list)-1:
            paramstr += '&'
    return url+paramstr


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    return res[0]


def get_response(endpoint, params):
    url = f"https://pro-api.coinmarketcap.com{endpoint}"
    headers = {
        # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-CMC_PRO_API_KEY': default_apikey,
    }

    ###################
    # Use this to generate url for browser if connection fails with python
    # print(render_url(endpoint=endpoint,params=params))
    # exit()
    ###################

    response = requests.get(url, params=params, headers=headers)

    # print(kargs)
    # print(response.url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def is_similar_substring(sub: str, sup: str, tolerance: int = 1):
    pattern_str = f"(?:{sub})"+"{e<="+f"{tolerance}"+"}"
    return regex.search(pattern_str, sup) != None


def normalize_param_for_interval(string: str, l: list, tolerance: int = 2):
    for i in l:
        if is_similar_substring(i, string, tolerance):
            return i


def normalize_param_substring(string: str, l: list, tolerance: int = 2):
    templist = []
    for i in l:
        if is_similar_substring(i, string, tolerance):
            templist.append(i)
    return ','.join(templist)


def get_cryptocurrency_categories(
    apikey: str = default_apikey,
    start: int = 1,
    limit: int = 10,
    id: str = '',
    slug: str = '',
    symbol: str = '',
):
    endpoint = '/v1/cryptocurrency/categories'
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'limit': limit,
        'start': start,
        'id': id,
        'slug': slug,
        'symbol': symbol,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_cryptocurrency_category(
    apikey: str = default_apikey,
    id: str = '',
    start: int = 1,
    limit: int = 10,
):
    endpoint = '/v1/cryptocurrency/category'
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'limit': limit,
        'start': start,
        'id': id,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    limit = limit if limit <= 1000 else 1000
    limit = limit if limit >= 1 else 1
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_cryptocurrency_coinmarketcap_id_map(
    apikey: str = default_apikey,
    listing_status: str = 'active',
    start: int = 1,
    limit: int = 10,
    if_sort_by_id: bool = True,
    symbol: str = '',
    aux: str = '',

):
    endpoint = '/v1/cryptocurrency/map'

    sort = 'id' if if_sort_by_id else 'cmc_rank'
    limit = limit if limit <= 5000 else 5000
    limit = limit if limit >= 1 else 1
    listing_status = normalize_param_substring(
        listing_status, ['active', 'inactive', 'untracked'], 0)
    aux = normalize_param_substring(
        aux, ['platform', 'first_historical_data', 'last_historical_data', 'is_active', 'status'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'limit': limit,
        'start': start,
        'listing_status': listing_status,
        'aux': aux,
        'symbol': symbol,
        'sort': sort,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_cryptocurrency_metadata_v2(
    apikey: str = default_apikey,
    id: str = '',
    slug: str = '',
    symbol: str = '',
    address: str = '',
    skip_invalid: bool = False,
    aux: str = '',

):
    endpoint = '/v2/cryptocurrency/info'

    aux = normalize_param_substring(
        aux, ['urls', 'logo', 'description', 'tags', 'platform', 'date_added', 'notice', 'status'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'id': id,
        'slug': slug,
        'symbol': symbol,
        'address': address,
        'skip_invalid': skip_invalid,
        'aux': aux,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_cryptocurrency_listing_latest(
    apikey: str = default_apikey,
    start: int = 1,
    limit: int = 50,
    price_min: int = None,
    prive_max: int = None,
    market_cap_min: int = None,
    market_cap_max: int = None,
    volume_24h_min: int = None,
    volume_24h_max: int = None,
    circulating_supply_min: int = None,
    circulating_supply_max: int = None,
    percent_change_24h_min: int = None,
    percent_change_24h_max: int = None,
    sort: str = 'market_cap',
    if_sort_asc: bool = False,
    cryptocurrency_type: str = 'all',
    tag: str = 'all',
    aux: str = 'num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply'
):
    endpoint = '/v1/cryptocurrency/listings/latest'

    sort = normalize_param_for_interval(sort, ["name", "symbol", "date_added", "market_cap", "market_cap_strict", "price", "circulating_supply", "total_supply", "max_supply",
                                        "num_market_pairs", "volume_24h", "percent_change_1h", "percent_change_24h", "percent_change_7d", "market_cap_by_total_supply_strict", "volume_7d""volume_30d"])
    sort_dir = 'asc' if if_sort_asc else 'desc'
    cryptocurrency_type = normalize_param_for_interval(
        cryptocurrency_type, ["all", "coins", "tokens"])
    tag = normalize_param_for_interval(tag, ["all", "defi", "filesharing"])
    aux = normalize_param_substring(aux, ['num_market_pairs', 'cmc_rank', 'date_added', 'tags', 'platform', 'max_supply', 'circulating_supply', 'total_supply',
                                    'market_cap_by_total_supply', 'volume_24h_reported', 'volume_7d', 'volume_7d_reported', 'volume_30d', 'volume_30d_reported', 'is_market_cap_included_in_calc'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'start': start,
        'limit': limit,
        'price_min': price_min,
        'prive_max': prive_max,
        'market_cap_min': market_cap_min,
        'market_cap_max': market_cap_max,
        'volume_24h_min': volume_24h_min,
        'volume_24h_max': volume_24h_max,
        'circulating_supply_max': circulating_supply_max,
        'circulating_supply_min': circulating_supply_min,
        'percent_change_24h_min': percent_change_24h_min,
        'percent_change_24h_max': percent_change_24h_max,
        'sort': sort,
        'sort_dir': sort_dir,
        'cryptocurrency_type': cryptocurrency_type,
        'tag': tag,
        'aux': aux,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_cryptocurrency_quotes_latest_v2(
    apikey: str = default_apikey,
    id: str = '',
    slug: str = '',
    symbol: str = '',
    skip_invalid: bool = True,
    aux: str = 'num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,is_active,is_fiat',

):
    endpoint = '/v2/cryptocurrency/quotes/latest'

    aux = normalize_param_substring(aux, ['num_market_pairs', 'cmc_rank', 'date_added', 'tags', 'platform', 'max_supply', 'circulating_supply', 'total_supply',
                                    'market_cap_by_total_supply', 'volume_24h_reported', 'volume_7d', 'volume_7d_reported', 'volume_30d', 'volume_30d_reported', 'is_active', 'is_fiat'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'id': id,
        'slug': slug,
        'symbol': symbol,
        'skip_invalid': skip_invalid,
        'aux': aux,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_coinmarketmap_id_map_fiat(
    apikey: str = default_apikey,
    start: int = None,
    limit: int = None,
    if_sort_by_id: bool = True,
    include_metals: bool = False,
):
    endpoint = '/v1/fiat/map'

    sort = 'id' if if_sort_by_id else 'name'

    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'start': start,
        'limit': limit,
        'sort': sort,
        'include_metals': include_metals,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_exchange_assets(
    apikey: str = default_apikey,
    id: str = '',
):
    endpoint = '/v1/exchange/assets'

    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'id': id,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_exchange_metadata(
    apikey: str = default_apikey,
    id: str = '',
    slug: str = '',
    aux: str = '',
):
    endpoint = '/v1/exchange/info'

    aux = normalize_param_substring(
        aux, ['urls', 'logo', 'description', 'date_launched', 'notice', 'status'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'id': id,
        'slug': slug,
        'aux': aux,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def get_coinmarketmap_id_map_exchange(
    apikey: str = default_apikey,
    listing_status: str = 'active',
    slug: str = '',
    start: int = 1,
    limit: int = 10,
    if_sort_by_id: bool = True,
    crypto_id: str = '',
    aux: str = '',

):
    endpoint = '/v1/exchange/map'

    sort = 'id' if if_sort_by_id else 'volume_24h'
    limit = limit if limit <= 5000 else 5000
    limit = limit if limit >= 1 else 1
    listing_status = normalize_param_substring(
        listing_status, ['active', 'inactive', 'untracked'], 0)
    aux = normalize_param_substring(
        aux, ['first_historical_data', 'last_historical_data', 'is_active', 'status'])
    queryparams = {
        'CMC_PRO_API_KEY': apikey,
        'limit': limit,
        'start': start,
        'listing_status': listing_status,
        'aux': aux,
        'slug': slug,
        'crypto_id': crypto_id,
        'sort': sort,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        endpoint=endpoint,
        params=queryparams
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


def file_print(t):
    with open('text.txt', 'w') as f:
        f.write(json.dumps(t, indent=4))


if __name__ == '__main__':
    # pretty_print(get_cryptocurrency_categories(limit=10))
    # pretty_print(get_cryptocurrency_category(id="64c7867acad87e003b856825"))
    # pretty_print(get_cryptocurrency_coinmarketcap_id_map(listing_status='active,,inactive',aux='platform,is_active'))
    # pretty_print(get_cryptocurrency_metadata_v2(slug='bitcoin,ethereum',aux='logo,description'))
    # pretty_print(get_cryptocurrency_listing_latest(percent_change_24h_min=50,sort='symbol',aux='logo,description'))
    # pretty_print(get_cryptocurrency_quotes_latest_v2(slug='bitcoin,ethereum',aux='cmc_rank,date_added'))
    # pretty_print(get_coinmarketmap_id_map_fiat(include_metals=True))
    # pretty_print(get_exchange_assets(id='270'))
    # pretty_print(get_exchange_metadata(slug='binance,gdax'))
    pretty_print(get_coinmarketmap_id_map_exchange(
        listing_status='active,,inactive', crypto_id='1', aux='last_historical_data'))
