import requests
from typing import Optional


def get_response(url, params={}, headers={}):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://api.travelpayouts.com/data"
TYPE2FILE = {
    "country": "/en/countries.json",
    "city": "/en/cities.json",
    "airport": "/en/airports.json",
    "airline": "/en/airlines.json",
    "alliance": "/en/alliances.json",
    "airplane": "/planes.json",
    "route": "/routes.json"
}


def get_json_data(query, search_type, key):
    if key not in ("name", "code"):
        return {"error": "key should be either name or code."}
    try:
        response = get_response(BASE_URL + TYPE2FILE[search_type])
        for e in response:
            if (key == "name" and e["name"] == query) \
                    or (key == "code" and e["code"] == query):
                return e
        if key == "name":
            return {"error": f"The input {query} may not be the name of any {search_type}."}
        else:
            return {"error": f"The input IATA code {query} may not correspond to any {search_type}."}
    except:
        return {"error": "Response error."}


def search_country(query: str, key: str = "name"):
    return get_json_data(query, "country", key)


def search_city(query: str, key: str = "name"):
    return get_json_data(query, "city", key)


def search_airport(query: str, key: str = "name"):
    return get_json_data(query, "airport", key)


def search_airline(query: str, key: str = "name"):
    return get_json_data(query, "airline", key)


def search_alliance(query: str):
    return get_json_data(query, "alliance", "name")


def search_airplane(query: str, key: str = "name"):
    return get_json_data(query, "airplane", key)


def search_routes(airline: Optional[str] = None, depart_airport: Optional[str] = None,
                  arrival_airport: Optional[str] = None, max_transfers: Optional[int] = None,
                  page: int = 0, page_size: int = 10):
    try:
        start = max(page * page_size, 0)
        end = max((page + 1) * page_size, start)
        if end == start:
            return []
        response = get_response(BASE_URL + TYPE2FILE["route"])
        final_results = []
        count = 0
        for route in response:
            if (not airline or route["airline_iata"] == airline) and (not depart_airport or route["departure_airport_iata"] == depart_airport) \
                    and (not arrival_airport or route["arrival_airport_iata"] == arrival_airport) and (max_transfers is None or route["transfers"] <= max_transfers):
                if count >= start:
                    final_results.append(route)
                    count += 1
                    if count >= end:
                        return final_results
        return final_results
    except:
        return {"error": "Response error."}


if __name__ == "__main__":
    # print(search_country("IN", "code"))
    # print(search_city("Shanghai"))
    print(search_airport("Kruger Mpumalanga International Airport"))
    # print(search_airline("Calima Aviacion S.L"))
    # print(search_alliance("OneWorld"))
    # print(search_airplane("767", "code"))
    # print(search_routes())
