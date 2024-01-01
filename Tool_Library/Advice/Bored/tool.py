import requests


url = "http://www.boredapi.com/api/activity/"


def get_response(**kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_random_event():
    return get_response()


def get_activity_by_key(key: int):
    return get_response(key=key)


def get_activity_by_type(type: str):
    return get_response(type=type)


def get_activity_by_participants(participants: int):
    return get_response(participants=participants)


def get_activity_by_price(price: float):
    return get_response(price=price)


def get_activity_by_price_range(minprice: float, maxprice: float):
    return get_response(minprice=minprice, maxprice=maxprice)


def get_activity_by_accessibility(accessibility: float):
    return get_response(accessibility=accessibility)


def get_activity_by_accessibility_range(minaccessibility: float, maxaccessibility: float):
    return get_response(minaccessibility=minaccessibility, maxaccessibility=maxaccessibility)


if __name__ == '__main__':
    # print(get_random_event())
    # print(get_activity_by_key(5881028))
    # print(get_activity_by_price(0))
    # print(get_activity_by_price_range(0.2, 0.9))
    # print(get_activity_by_type('recreational'))
    print(get_activity_by_participants(participants=2))
    # print(get_activity_by_accessibility(0.2))
    # print(get_activity_by_accessibility_range(0.3, 0.8))
