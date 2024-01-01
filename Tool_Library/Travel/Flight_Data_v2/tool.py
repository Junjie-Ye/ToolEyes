import json
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


BASE_URL = "https://api.travelpayouts.com/v2"


def cheapest_tickets(origin: Optional[str] = None, destination: Optional[str] = None, period_type: str = "year", beginning_of_period: Optional[str] = None, one_way: bool = False,
                     sorting: str = "price", page: int = 1, limit: int = 10, currency: str = "RUB", token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "period_type": period_type,
        "beginning_of_period": beginning_of_period,
        "one_way": one_way,
        "sorting": sorting,
        "page": page,
        "limit": limit,
        "currency": currency,
        "show_to_affiliates": True
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/latest", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def prices_calendar_month(origin: str, destination: str, month: Optional[str] = None,
                          currency: str = "RUB", token: str = ""):
    tomorrow = datetime.now() + timedelta(days=1)
    if not month:
        month = f"{tomorrow.year}-{'0' + str(tomorrow.month) if tomorrow.month < 10 else tomorrow.month}"
    params = {
        "origin": origin,
        "destination": destination,
        "month": month,
        "currency": currency,
        "show_to_affiliates": True
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/month-matrix", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def direction_prices(origin: str, destination: str, limit: int = 10, depart_date: Optional[str] = None,
                     return_date: Optional[str] = None, flexibility: int = 0, distance: int = 1,
                     currency: str = "RUB", token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "limit": limit,
        "depart_date": depart_date,
        "return_date": return_date,
        "flexibility": flexibility,
        "distance": distance,
        "currency": currency,
        "show_to_affiliates": True
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(
        BASE_URL + "/prices/nearest-places-matrix", params, headers)
    try:
        return response["prices"]
    except:
        return response["error"]


def prices_calendar_week(origin: str, destination: str, depart_date: Optional[str] = None, return_date: Optional[str] = None,
                         currency: str = "RUB", token: str = ""):
    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
        "currency": currency,
        "show_to_affiliates": True
    }
    params = {k: v for k, v in params.items() if v is not None}
    headers = generate_headers(token)

    response = get_response(BASE_URL + "/prices/week-matrix", params, headers)
    try:
        return response["data"]
    except:
        return response["error"]


def get_location_by_ip(ip: Optional[str] = None, token: str = ""):
    params = {
        "locale": "en",
        "callback": "useriata",
    }
    if ip:
        params["ip"] = ip

    # response: "useriata({...})
    response: str = get_response(
        "https://www.travelpayouts.com/whereami", params)
    return json.loads(response[9: -1]) if response.startswith("useriata") else response


if __name__ == "__main__":
    # print(cheapest_tickets())
    # print(prices_calendar_month("LED", "HKT", currency="USD"))
    # print(direction_prices("LED", "HKT", currency="USD"))
    # print(prices_calendar_week("LED", "HKT", currency="USD"))
    print(get_location_by_ip())
