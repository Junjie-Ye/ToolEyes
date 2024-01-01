import requests
import json
import csv
import regex
import datetime
from dateutil.parser import parse


locale_list_doc = 'https://docs.developer.yelp.com/docs/resources-supported-locales'

locale_list = [
    'cs_CZ',
    'da_DK',
    'de_AT',
    'de_CH',
    'de_DE',
    'en_AU',
    'en_BE',
    'en_CA',
    'en_CH',
    'en_GB',
    'en_HK',
    'en_IE',
    'en_MY',
    'en_NZ',
    'en_PH',
    'en_SG',
    'en_US',
    'es_AR',
    'es_CL',
    'es_ES',
    'es_MX',
    'fi_FI',
    'fil_PH',
    'fr_BE',
    'fr_CA',
    'fr_CH',
    'fr_FR',
    'it_CH',
    'it_IT',
    'ja_JP',
    'ms_MY',
    'nb_NO',
    'nl_BE',
    'nl_NL',
    'pl_PL',
    'pt_BR',
    'pt_PT',
    'sv_FI',
    'sv_SE',
    'tr_TR',
    'zh_HK',
    'zh_TW'
]

attributes_list = [
    'hot_and_new',
    'request_a_quote',
    'reservation',
    'waitlist_reservation',
    'deals',
    'gender_neutral_restrooms',
    'open_to_all',
    'wheelchair_accessible'
]


doc_url = 'https://docs.developer.yelp.com/reference/v3_business_search'
base_url = 'https://api.yelp.com/v3'
client_id = 'z2Keeyjq_fRMMaeCOfdKng'
default_apikey = ''


def remove_empty_value_for_dict(d: dict):
    temp = [d]
    res = list(filter(
        None, ({key: val for key, val in sub.items() if val} for sub in temp)))
    if len(res):
        return res[0]
    else:
        return {}


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


def normalize_param_for_interval(string: str, l: list, tolerance: int = 2):
    for i in l:
        if is_similar_substring(i, string, tolerance):
            return i


def yelp_search(
    apikey: str = default_apikey,

    location: str = '',
    latitude: int = 0,
    longitude: int = 0,
    term: str = '',
    radius: int = 0,
    categories: str = '',
    locale: str = '',
    price: str = '',
    open_now: bool = True,
    open_at: str = '',
    attributes: str = '',
    sort_by: str = 'best_match',
    device_platform: str = '',
    reservation_date: str = '',
    reservation_covers: int = 0,
    matches_party_size_param: bool = True,
    limit: int = 20,
    offset: int = 0,
):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }

    locale = normalize_param_for_interval(locale, locale_list, 0)

    price_list = []
    for i in range(4):
        if str(i+1) in price:
            price_list.append(str(i+1))
    price = ','.join(price_list)

    try:
        open_at = int(datetime.datetime.timestamp(parse(open_at))*1000)
    except:
        open_at = 0

    attributes = normalize_param_for_interval(attributes, attributes_list)

    sort_by = normalize_param_for_interval(
        sort_by, ['best_match', 'rating', 'review_count', 'distance'])

    try:
        reservation_date = dateparser(reservation_date)
    except:
        reservation_date = ''

    queryparams = {
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'term': term,
        'radius': radius,
        'categories': categories,
        'locale': locale,
        'price': price,
        'open_now': open_now,
        'open_at': open_at,
        'attributes': attributes,
        'sort_by': sort_by,
        'device_platform': device_platform,
        'reservation_date': reservation_date,
        'reservation_covers': reservation_covers,
        'matches_party_size_param': matches_party_size_param,
        'limit': limit,
        'offset': offset,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_phone_search(
    apikey: str = default_apikey,

    phone: str = '',
    locale: str = '',
):
    url = "https://api.yelp.com/v3/businesses/search/phone"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }
    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
        'phone': phone,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_business_details(
    apikey: str = default_apikey,

    business_id_or_alias: str = '',
    locale: str = '',
    device_platform: str = '',
):
    url = f"https://api.yelp.com/v3/businesses/{business_id_or_alias}"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }

    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
        'device_platform': device_platform,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_food_delivery_search(
    apikey: str = default_apikey,

    location: str = '',
    latitude: int = 0,
    longitude: int = 0,
    term: str = '',
    categories: str = '',
    price: str = '',
):
    transaction_type = 'delivery'
    url = f"https://api.yelp.com/v3/transactions/{transaction_type}/search"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }

    price_list = []
    for i in range(4):
        if str(i+1) in price:
            price_list.append(str(i+1))
    price = ','.join(price_list)

    queryparams = {
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'term': term,
        'categories': categories,
        'price': price,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_reviews(
    apikey: str = default_apikey,

    business_id_or_alias: str = '',
    locale: str = '',
    if_sort_by_auto: bool = True,
    limit: int = 20,
    offset: int = 0,
):
    url = f"https://api.yelp.com/v3/businesses/{business_id_or_alias}/reviews"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }
    sort_by = 'yelp_sort' if if_sort_by_auto else 'newesta'

    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
        'sort_by': sort_by,
        'limit': limit,
        'offset': offset,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_event_search(
    apikey: str = default_apikey,

    locale: str = '',
    limit: int = 20,
    offset: int = 0,
    if_sort_by_desc: bool = True,
    if_sort_on_popularity: bool = True,
    start_date: str = '',
    end_date: str = '',
    categories: str = '',
    excluded_events: str = '',
    location: str = '',
    latitude: int = 0,
    longitude: int = 0,
    radius: int = 0,
):
    url = "https://api.yelp.com/v3/events"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }

    locale = normalize_param_for_interval(locale, locale_list, 0)

    try:
        start_date = int(datetime.datetime.timestamp(parse(start_date))*1000)
    except:
        start_date = 0
    try:
        end_date = int(datetime.datetime.timestamp(parse(end_date))*1000)
    except:
        end_date = 0

    sort_on = 'popularity'if if_sort_on_popularity else 'time_start'
    sort_by = 'desc'if if_sort_by_desc else 'asc'

    queryparams = {
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'excluded_events': excluded_events,
        'start_date': start_date,
        'end_date': end_date,
        'radius': radius,
        'categories': categories,
        'locale': locale,
        'sort_on': sort_on,
        'sort_by': sort_by,
        'limit': limit,
        'offset': offset,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_event_details(
    apikey: str = default_apikey,

    event_id: str = '',
    locale: str = '',
):
    url = f"https://api.yelp.com/v3/events/{event_id}"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }
    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def yelp_all_categories(
    apikey: str = default_apikey,

    locale: str = '',
):
    url = f"https://api.yelp.com/v3/categories"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }
    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )

def yelp_category_details(
    apikey: str = default_apikey,

    alias:str='',
    locale: str = '',
):
    url = f"https://api.yelp.com/v3/categories/{alias}"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }
    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'locale': locale,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )

def yelp_autocomplete(
    apikey: str = default_apikey,

    text: str = '',
    latitude: int = 0,
    longitude: int = 0,
    locale: str = '',
):
    url = "https://api.yelp.com/v3/autocomplete"
    headers = {
        "accept": "application/json",
        "Authorization": apikey,
    }

    locale = normalize_param_for_interval(locale, locale_list, 0)

    queryparams = {
        'text': text,
        'latitude': latitude,
        'longitude': longitude,
        'locale': locale,
    }
    queryparams = remove_empty_value_for_dict(queryparams)
    return get_response(
        url=url,
        headers=headers,
        params=queryparams
    )


def pretty_print(t):
    print(json.dumps(t, indent=4))


def file_print(t):
    with open('text.txt', 'w') as f:
        f.write(json.dumps(t, indent=4))


if __name__ == '__main__':
    # file_print(yelp_search(price='12',location='NYC'))
    # file_print(yelp_phone_search(phone='+14159083801'))
    # file_print(yelp_business_details(business_id_or_alias='4kMBvIEWPxWkWKFN__8SxQ'))
    # file_print(yelp_food_delivery_search(location='NYC',))
    # file_print(yelp_reviews(business_id_or_alias='MpF9j5-fBH0H6L9AzzyArA'))
    # file_print(yelp_event_search(locale='en-US',limit=10,if_sort_by_desc=True))
    # file_print(yelp_event_details(event_id='austin-rsvps-closed-yelp-austins-backyard-blowout'))
    file_print(yelp_all_categories(locale='en-US'))
    # file_print(yelp_category_details(locale='en-US',alias='localservices'))
    # file_print(yelp_autocomplete(locale='en-US',text='hamberg'))
