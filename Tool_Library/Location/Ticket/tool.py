import requests


def get_response(url, kargs):
    headers = {
        'Host': 'app.ticketmaster.com',
        'X-Target-URI': 'https://app.ticketmaster.com',
        # 'Connection':'Keep-Alive'
    }
    response = requests.get(url, params=kargs, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_international_response(url, kargs):
    headers = {
        'Host': 'app.ticketmaster.eu/mfxapi/v2',
        'X-Target-URI': 'https://app.ticketmaster.eu',
        # 'Connection':'Keep-Alive'
    }
    response = requests.get(url, params=kargs, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_post_response(url, arg_dict=None, file=None):
    response = requests.post(url, data=arg_dict, files=file)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def event_search(id: str = None, keyword: str = None, attractionId: str = None, venueId: str = None,
                 postalCode: str = None, radius: str = None, unit: str = None, source: str = None, locale: str = None,
                 marketId: str = None, startDateTime: str = None, endDateTime: str = None, size: str = '3', page: str = None, sort_by: str = None,
                 onsaleStartDateTime: str = None, onsaleEndDateTime: str = None, city: list[str] = None, countryCode: str = None,
                 stateCode: str = None, classificationId: list[str] = None,
                 segmentId: list[str] = None, includeFamily: str = None,
                 genreId: list[str] = None, subGenreId: list[str] = None,
                 geoPoint: str = None, domain: list[str] = None):
    url = "https://app.ticketmaster.com/discovery/v2/events.json?"
    kv_dict = []
    kv_dict.append(('apikey', ""))
    kv_dict.append(('id', id))
    kv_dict.append(('sort', sort_by))
    kv_dict.append(('keyword', keyword))
    kv_dict.append(('attractionId', attractionId))
    kv_dict.append(('venueId', venueId))
    kv_dict.append(('postalCode', postalCode))
    kv_dict.append(('radius', radius))
    kv_dict.append(('unit', unit))
    kv_dict.append(('source', source))
    kv_dict.append(('locale', locale))
    kv_dict.append(('marketId', marketId))
    kv_dict.append(('startDateTime', startDateTime))
    kv_dict.append(('endDateTime', endDateTime))
    kv_dict.append(('size', size))
    kv_dict.append(('page', page))
    kv_dict.append(('onsaleStartDateTime', onsaleStartDateTime))
    kv_dict.append(('onsaleEndDateTime', onsaleEndDateTime))
    kv_dict.append(('city', city))
    kv_dict.append(('countryCode', countryCode))
    kv_dict.append(('stateCode', stateCode))
    kv_dict.append(('classificationId', classificationId))
    kv_dict.append(('segmentId', segmentId))
    kv_dict.append(('includeFamily', includeFamily))
    kv_dict.append(('genreId', genreId))
    kv_dict.append(('subGenreId', subGenreId))
    kv_dict.append(('geoPoint', geoPoint))
    kv_dict.append(('domain', domain))

    events = get_response(url, kv_dict)['_embedded']['events']
    for i in range(len(events)):
        events[i]['images'] = events[i]['images'][:min(
            3, len(events[i]['images']))]
        # for j in range(len(events[i]["_embedded"]['attractions'])):
        #    events[i]["_embedded"]['attractions'][j]['images'] = events[i]["_embedded"]['attractions'][j]['images'][:min(3,len(events[i]["_embedded"]['attractions'][j]['images']))]
    return events


def get_event_details(id: str, locale: str = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/events/{id}?"
    kv_dict = []
    kv_dict.append(('locale', locale))
    kv_dict.append(('domian', domain))
    kv_dict.append(('apikey', ""))
    return get_response(url, kv_dict)


def attraction_search(id: str = None, keyword: str = None, source: str = None, locale: str = None,
                      size: str = None, page: str = None, sort_by: str = None, classificationId: list[str] = None,
                      segmentId: list[str] = None, includeFamily: str = None,
                      genreId: list[str] = None, subGenreId: list[str] = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/attractions/{id}?"
    kv_dict = []
    kv_dict.append(('apikey', ""))
    kv_dict.append(('id', id))
    kv_dict.append(('sort', sort_by))
    kv_dict.append(('keyword', keyword))
    kv_dict.append(('source', source))
    kv_dict.append(('locale', locale))
    kv_dict.append(('size', size))
    kv_dict.append(('page', page))
    kv_dict.append(('classificationId', classificationId))
    kv_dict.append(('segmentId', segmentId))
    kv_dict.append(('includeFamily', includeFamily))
    kv_dict.append(('genreId', genreId))
    kv_dict.append(('subGenreId', subGenreId))
    kv_dict.append(('domain', domain))
    return get_response(url, kv_dict)


def get_attraction_details(id: str, locale: str = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/attractions/{id}?"
    kv_dict = []
    kv_dict.append(('locale', locale))
    kv_dict.append(('domian', domain))
    kv_dict.append(('apikey', ""))
    return get_response(url, kv_dict)


def classification_search(id: str = None, keyword: str = None, source: str = None, locale: str = None,
                          size: str = None, page: str = None, sort_by: str = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/classifications?"
    kv_dict = []
    kv_dict.append(('apikey', ""))
    kv_dict.append(('id', id))
    kv_dict.append(('sort', sort_by))
    kv_dict.append(('keyword', keyword))
    kv_dict.append(('source', source))
    kv_dict.append(('locale', locale))
    kv_dict.append(('size', size))
    kv_dict.append(('page', page))
    kv_dict.append(('domain', domain))
    return get_response(url, kv_dict)


def get_claasificatioin_details(id: str, locale: str = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/classifications/{id}?"
    kv_dict = []
    kv_dict.append(('id', id))
    kv_dict.append(('locale', locale))
    kv_dict.append(('domian', domain))
    kv_dict.append(('apikey', ""))
    return get_response(url, kv_dict)


def venue_search(id: str = None, keyword: str = None, source: str = None, locale: str = None, radius: str = None, unit: str = None,
                 size: str = None, page: str = None, sort_by: str = None, domain: list[str] = None, geoPoint: str = None, countryCode: str = None,
                 stateCode: str = None,):
    url = f"https://app.ticketmaster.com/discovery/v2/venues?"
    kv_dict = []
    kv_dict.append(('apikey', ""))
    kv_dict.append(('radius', radius))
    kv_dict.append(('unit', unit))
    kv_dict.append(('id', id))
    kv_dict.append(('sort', sort_by))
    kv_dict.append(('keyword', keyword))
    kv_dict.append(('source', source))
    kv_dict.append(('locale', locale))
    kv_dict.append(('size', size))
    kv_dict.append(('page', page))
    kv_dict.append(('domain', domain))
    kv_dict.append(('geoPoint', geoPoint))
    kv_dict.append(('countryCode', countryCode))
    kv_dict.append(('stateCode', stateCode))
    return get_response(url, kv_dict)


def get_venue_details(id: str, locale: str = None, domain: list[str] = None):
    url = f"https://app.ticketmaster.com/discovery/v2/venues/{id}?"
    kv_dict = []
    kv_dict.append(('locale', locale))
    kv_dict.append(('domian', domain))
    kv_dict.append(('apikey', ""))
    return get_response(url, kv_dict)


def find_suggest(keyword: str = None, radius: str = None, unit: str = None, source: str = None, locale: str = None,
                 size: str = '3', page: str = None, countryCode: str = None,
                 segmentId: list[str] = None, resource: list[str] = None, startEndDateTime: list[str] = None,
                 geoPoint: str = None, domain: list[str] = None):
    url = "https://app.ticketmaster.com/discovery/v2/suggest?"
    kv_dict = []
    kv_dict.append(('apikey', ""))
    kv_dict.append(('keyword', keyword))
    kv_dict.append(('radius', radius))
    kv_dict.append(('unit', unit))
    kv_dict.append(('source', source))
    kv_dict.append(('locale', locale))
    kv_dict.append(('size', size))
    kv_dict.append(('page', page))
    kv_dict.append(('resource', resource))
    kv_dict.append(('startEndDateTime', startEndDateTime))
    kv_dict.append(('countryCode', countryCode))
    kv_dict.append(('segmentId', segmentId))
    kv_dict.append(('geoPoint', geoPoint))
    kv_dict.append(('domain', domain))
    events = get_response(url, kv_dict)['_embedded']
    for i in range(len(events['events'])):
        events['events'][i]['images'] = events['events'][i]['images'][:min(
            3, len(events['events'][i]['images']))]
        # for j in range(len(events['events'][i]["_embedded"]['attractions'])):
        #    events['events'][i]["_embedded"]['attractions'][j]['images'] = events['events'][i]["_embedded"]['attractions'][j]['images'][:min(3,len(events['events'][i]["_embedded"]['attractions'][j]['images']))]
    for i in range(len(events['products'])):
        events['products'][i]['images'] = events['products'][i]['images'][:min(
            3, len(events['products'][i]['images']))]
        # for j in range(len(events['events'][i]["_embedded"]['attractions'])):
        #    events['products'][i]["_embedded"]['attractions'][j]['images'] = events['products'][i]["_embedded"]['attractions'][j]['images'][:min(3,len(events['products'][i]["_embedded"]['attractions'][j]['images']))]

    for i in range(len(events['attractions'])):
        events['attractions'][i]['images'] = events['attractions'][i]['images'][:min(
            3, len(events['attractions'][i]['images']))]

    return events


if __name__ == '__main__':
    pass
    # print(find_suggest(keyword='picnic'))
    # print("\n")
    # print(get_event_details(id="vvG1HZ9YNxapWr"))
    # print(event_search())
    print(event_search(keyword='match'))
    # print(venue_search(keyword='theatre'))
