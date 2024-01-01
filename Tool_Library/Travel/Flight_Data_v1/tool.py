import requests
from typing import Optional
from datetime import datetime, timedelta


def get_response(url, params={}, headers={}):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def generate_headers(token):
    return {"x-access-token": token}


def cName2IATA(city_name: str):
    response = get_response(
        "https://api.travelpayouts.com/data/en/cities.json")
    for city in response:
        if city["name"] == city_name:
            return city["code"]

    return {"error": f"The input city {city_name} may not have an IATA code."}


BASE_URL = "https://api.travelpayouts.com/v1"


def cheapest_tickets(origin: str, destination: str, depart_date: Optional[str] = None, return_date: Optional[str] = None,
                     page: int = 1, currency: str = "RUB", token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
        "page": page,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/cheap", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def cheapest_direct_tickets(origin: str, destination: str, depart_date: Optional[str] = None, return_date: Optional[str] = None,
                            currency: str = "RUB", token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/direct", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def cheapest_tickets_each_day(origin: str, destination: str, depart_date: Optional[str] = None, return_date: Optional[str] = None,
                              calender_type: str = "departure_date", length: Optional[int] = None, currency: str = "RUB",
                              token: str = ""):
    tomorrow = datetime.now() + timedelta(days=1)
    default_date = f"{tomorrow.year}-{'0' + str(tomorrow.month) if tomorrow.month < 10 else tomorrow.month}-{'0' + str(tomorrow.day) if tomorrow.day < 10 else tomorrow.day}"
    if not depart_date or depart_date < default_date:
        depart_date = default_date
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
        "calender_type": calender_type,
        "length": length,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/calendar", params, headers)
    try:
        data = response["data"]
        min_keys = sorted(data)[:30]
        return {key: data[key] for key in min_keys}
    except:
        return response["error"]


def cheapest_tickets_each_month(origin: str, destination: str, currency: str = "RUB",
                                token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/monthly", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def popular_airline_routes(airline_code: str, limit: int = 10,
                           token: str = ""):
    params = {
        "airline_code": airline_code,
        "limit": limit
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/airline-directions", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def popular_directions_from_city(origin: str, limit: int = 10, currency: str = "RUB",
                                 token: str = ""):
    params = {
        "origin": origin,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/city-directions", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


if __name__ == "__main__":
    # print(cheapest_tickets("MOW", "HKT"))
    # print(cheapest_direct_tickets("MOW", "LED"))
    # print(cheapest_tickets_each_day("MOW", "BCN", currency="USD"))
    # print(cheapest_tickets_each_month("MOW", "BCN", currency="USD"))
    # print(popular_airline_routes("SU"))
    print(popular_directions_from_city("MOW", 2))
