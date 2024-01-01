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


BASE_URL = "http://engine.hotellook.com/api/v2"


def search_city_hotels(query: str, lookFor: str = "both", limit: int = 10):
    params = {
        "query": query,
        "lookFor": lookFor,
        "limit": limit
    }
    response = get_response(BASE_URL + "/lookup.json", params)
    try:
        return response["results"]
    except:
        return response


def display_hotels_prices(location: str, checkIn: Optional[str] = None, checkOut: Optional[str] = None, hotel: Optional[str] = None,
                          adults: int = 2, children: int = 0, infants: int = 0, limit: int = 4,
                          customerIp: Optional[str] = None, currency: Optional[str] = None):
    tomorrow = datetime.now() + timedelta(days=1)
    if not checkIn:
        checkIn = f"{tomorrow.year}-{'0' + str(tomorrow.month) if tomorrow.month < 10 else tomorrow.month}-{'0' + str(tomorrow.day) if tomorrow.day < 10 else tomorrow.day}"
    if not checkOut:
        try:
            date_checkIn = datetime.strptime(checkIn, "%Y-%m-%d")
            date_checkOut = date_checkIn + timedelta(days=3)
            checkOut = f"{date_checkOut.year}-{'0' + str(date_checkOut.month) if date_checkOut.month < 10 else date_checkOut.month}-{'0' + str(date_checkOut.day) if date_checkOut.day < 10 else date_checkOut.day}"
        except:
            return {"message": "checkIn: Must be formatted like yyyy-MM-dd", "status": "error", "errorCode": 2}

    params = {
        "location": location,
        "checkIn": checkIn,
        "checkOut": checkOut,
        "hotel": hotel,
        "adults": adults,
        "children": children,
        "infants": infants,
        "limit": limit,
        "customerIp": customerIp,
        "currency": currency
    }
    params = {k: v for k, v in params.items() if v is not None}
    return get_response(BASE_URL + "/cache.json", params)


def hotel_collection(id: str, token: str = ""):
    params = {
        "id": id,
        "token": token
    }
    return get_response("http://yasen.hotellook.com/tp/public/available_selections.json", params)


if __name__ == "__main__":
    # print(search_city_hotels("moscow"))
    # print(display_hotels_prices("Saint-Petersburg"))
    print(hotel_collection("12209"))
