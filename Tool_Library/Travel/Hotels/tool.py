import requests
from typing import Optional, List, Tuple


def get_response(url, params={}, headers={}):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def post_response(url, payload={}, headers={}):
    response = requests.post(url, json=payload, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://hotels4.p.rapidapi.com"
API_HOST = "hotels4.p.rapidapi.com"


def generate_get_headers(api_key):
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }


def generate_post_headers(api_key):
    return {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }


def get_sites(api_key: str = ""):
    response = get_response(BASE_URL + f"/v2/get-meta-data",
                            headers=generate_get_headers(api_key))
    return str(response.keys()) if "AR" in response else response


def get_meta_data(site: str, api_key: str = ""):
    response = get_response(BASE_URL + f"/v2/get-meta-data",
                            headers=generate_get_headers(api_key))
    if "AR" in response:
        return response[site] if site in response else {}
    return response


def search_locations(query: str, siteid: Optional[str] = None, locale: Optional[str] = None,
                     api_key: str = ""):
    params = {"q": query}
    if siteid is not None:
        params["siteid"] = siteid
    if locale is not None:
        params["locale"] = locale
    response = get_response(
        BASE_URL + f"/locations/v3/search", params, generate_get_headers(api_key))
    try:
        return response["sr"]
    except:
        return response


def list_properties(dest_regionId: str, check_in_date: Tuple[int, int, int], check_out_date: Tuple[int, int, int],
                    num_adults_list: List[int], children_ages_list: List[List[int]], currency: Optional[str] = None, eapid: Optional[int] = None,
                    siteId: Optional[int] = None, locale: Optional[str] = None, resultSize: int = 3, resultsStartingIndex: int = 0,
                    dest_coordinates: Optional[Tuple[int, int]] = None, sort: str = "PRICE_RELEVANT", hotelName: Optional[str] = None,
                    price: Optional[Tuple[int, int]] = None, guestRating: Optional[str] = None, accessibility: Optional[List[str]] = None,
                    travelerType: Optional[List[str]] = None, mealPlan: Optional[List[str]] = None, poi: Optional[str] = None,
                    regionId: Optional[str] = None, lodging: Optional[List[str]] = None, amenities: Optional[List[str]] = None,
                    star: Optional[List[str]] = None, paymentType: Optional[List[str]] = None, bedroomFilter: Optional[List[str]] = None,
                    availableFilter: Optional[str] = None, api_key: str = ""):
    if len(num_adults_list) != len(children_ages_list):
        return {"message": "Illegal parameter rooms. num_adults_list and children_ages_list should have the save length."}
    headers = generate_post_headers(api_key)
    destination = {}
    if dest_coordinates is not None:
        dest_coordinates = {
            "latitude": dest_coordinates[0],
            "longitude": dest_coordinates[1]
        }
        destination = {
            "regionId": dest_regionId,
            "coordinates": dest_coordinates
        }
    else:
        destination = {"regionId": dest_regionId}

    def list2param(array):
        return None if array is None or len(array) == 0 else array
    filters = {
        "hotelName": hotelName,
        "price": None if price is None else {
            "max": price[0],
            "min": price[1]
        },
        "guestRating": guestRating,
        "accessibility": list2param(accessibility),
        "travelerType": list2param(travelerType),
        "mealPlan": list2param(mealPlan),
        "poi": poi,
        "regionId": regionId,
        "lodging": list2param(lodging),
        "amenities": list2param(amenities),
        "star": list2param(star),
        "paymentType": list2param(paymentType),
        "bedroomFilter": list2param(bedroomFilter),
        "availableFilter": availableFilter
    }
    filters = {k: v for k, v in filters.items() if v is not None}

    payload = {
        "currency": currency,
        "eapid": eapid,
        "siteId": siteId,
        "locale": locale,
        "resultsSize": resultSize,
        "resultsStartingIndex": resultsStartingIndex,
        "destination": destination,
        "checkInDate": {
            "day": check_in_date[0],
            "month": check_in_date[1],
            "year": check_in_date[2]
        },
        "checkOutDate": {
            "day": check_out_date[0],
            "month": check_out_date[1],
            "year": check_out_date[2]
        },
        "rooms": [{
            "adults": num_adults,
            "children": [{"age": age} for age in children_ages_list[i]]
        } for i, num_adults in enumerate(num_adults_list)],
        "sort": sort,
        "filters": filters if len(filters) > 0 else None
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    response = post_response(
        BASE_URL + f"/properties/v2/list", payload, headers)
    try:
        return response["data"]["propertySearch"]["properties"]
    except:
        return response


def get_property_offers(propertyId: str, dest_regionId: str, check_in_date: Tuple[int, int, int], check_out_date: Tuple[int, int, int],
                        num_adults_list: List[int], children_ages_list: List[List[int]], currency: Optional[str] = None, eapid: Optional[int] = None,
                        siteId: Optional[int] = None, locale: Optional[str] = None, dest_coordinates: Optional[Tuple[int, int]] = None,
                        api_key: str = ""):
    if len(num_adults_list) != len(children_ages_list):
        return {"message": "Illegal parameter rooms. num_adults_list and children_ages_list should have the save length."}
    headers = generate_post_headers(api_key)
    destination = {}
    if dest_coordinates is not None:
        dest_coordinates = {
            "latitude": dest_coordinates[0],
            "longitude": dest_coordinates[1]
        }
        destination = {
            "regionId": dest_regionId,
            "coordinates": dest_coordinates
        }
    else:
        destination = {"regionId": dest_regionId}

    payload = {
        "propertyId": propertyId,
        "currency": currency,
        "eapid": eapid,
        "siteId": siteId,
        "locale": locale,
        "destination": destination,
        "checkInDate": {
            "day": check_in_date[0],
            "month": check_in_date[1],
            "year": check_in_date[2]
        },
        "checkOutDate": {
            "day": check_out_date[0],
            "month": check_out_date[1],
            "year": check_out_date[2]
        },
        "rooms": [{
            "adults": num_adults,
            "children": [{"age": age} for age in children_ages_list[i]]
        } for i, num_adults in enumerate(num_adults_list)]
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    response = post_response(
        BASE_URL + "/properties/v2/get-offers", payload, headers)
    try:
        return response["data"]["propertyOffers"]
    except:
        return response


def resolve_url(id: str, siteid: Optional[int] = None, locale: Optional[str] = None,
                api_key: str = ""):
    headers = generate_get_headers(api_key)
    params = {
        "id": id,
        "siteid": siteid,
        "locale": locale
    }
    params = {k: v for k, v in params.items() if v is not None}
    return get_response(BASE_URL + "/properties/v2/resolve-url", params, headers)


def get_reviews_summary(propertyId: str, currency: Optional[str] = None, eapid: Optional[int] = None, locale: Optional[str] = None,
                        siteId: Optional[int] = None, api_key: str = ""):
    headers = generate_post_headers(api_key)
    payload = {
        "propertyId": propertyId,
        "siteId": siteId,
        "currency": currency,
        "eapid": eapid,
        "locale": locale
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    response = post_response(
        BASE_URL + "/reviews/v3/get-summary", payload, headers)
    try:
        return response["data"]["propertyReviewSummaries"]
    except:
        return response


if __name__ == "__main__":
    # print(get_sites())
    # print(get_meta_data("CO"))
    # print(search_location("new york", 300000001))
    # print(list_properties("6054439", [10, 10, 2022], [15, 10, 2022], [2], [[5, 7]]))
    # print(get_property_offers("9209612", "6054439", [6, 10, 2023], [9, 10, 2023], [2, 2], [[5, 7], []]))
    # print(resolve_url("ho546370"))
    print(get_reviews_summary("9209612"))
