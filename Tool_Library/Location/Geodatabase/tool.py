import requests


def get_response(url, kargs):
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    response = requests.get(url, params=kargs, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_post_response(url, arg_dict=None, file=None):
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    response = requests.post(url, data=arg_dict, headers=headers, files=file)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def find_countries(namePrefix: str = None, sort_by: str = None, limit: int = None, offset: int = None, currencyCode: str = None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries?"
    kv_dict = []
    kv_dict.append(('currencyCode', currencyCode))
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    kv_dict.append(('namePrefix', namePrefix))
    kv_dict.append(('sort', sort_by))
    return get_response(url, kv_dict)['data']


def find_places(namePrefix: str = None, sort_by: str = None, limit: int = None, offset: int = None, location: str = None, minPopulation: int = None, maxPopulation: int = None, radius: int = None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/places?"
    start = True
    kv_dict = []
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    kv_dict.append(('namePrefix', namePrefix))
    kv_dict.append(('location', location))
    kv_dict.append(('radius', radius))
    kv_dict.append(('minPopulation', minPopulation))
    kv_dict.append(('maxPopulation', maxPopulation))
    kv_dict.append(('sort', sort_by))
    return get_response(url, kv_dict)['data']


def find_regions(countryId: str, limit: int = None, offset: int = None, namePrefix: str = None):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{countryId}/regions?"
    kv_dict = []
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    kv_dict.append(('namePrefix', namePrefix))
    return get_response(url, kv_dict)['data']


def get_country_details(countryId: str):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{countryId}?"
    kv_dict = []
    return get_response(url, kv_dict)


def get_place_details(placeId: int):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/places/{placeId}"
    kv_dict = []
    return get_response(url, kv_dict)


def get_region_details(countryId: str, regionCode: str):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{countryId}/regions/{regionCode}"
    kv_dict = []
    return get_response(url, kv_dict)


def get_currencies(countryId: str = None, limit: int = None, offset: int = None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/locale/currencies?"
    kv_dict = []
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    kv_dict.append(('countryId', countryId))
    return get_response(url, kv_dict)


def get_locales(limit: int = None, offset: int = None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/locale/locales?"
    kv_dict = []
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    return get_response(url, kv_dict)


def get_time_zones(limit: int = None, offset: int = None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/locale/timezones?"
    kv_dict = []
    kv_dict.append(('limit', limit))
    kv_dict.append(('offset', offset))
    return get_response(url, kv_dict)


def get_time_zone_date_time(zoneId: str):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/locale/timezones/{zoneId}/dateTime"
    kv_dict = []
    return get_response(url, kv_dict)


def get_university_infomation(name: str = None, country: str = None):
    url = "http://universities.hipolabs.com/search"
    kv_dict = []
    kv_dict.append(('name', name))
    kv_dict.append(('country', country))

    return get_response(url, kv_dict)


if __name__ == '__main__':
    pass
    # print(find_countries(limit=5,offset=2))
    # print(find_places(limit=2))
    # print(find_regions(countryId="US",limit=5,offset=2))
    # print(get_country_details(countryId="FR"))
    # print(get_place_details(placeId=3710202))
    # print(get_region_details(countryId="CN",regionCode="BJ"))
    # print(get_currencies(countryId='US'))
    # print(get_time_zone_date_time(zoneId="America__Marigot"))
    # print(get_university_infomation(country='Ecuador'))
