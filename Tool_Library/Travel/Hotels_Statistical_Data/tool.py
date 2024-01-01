import requests
from typing import Tuple
from bs4 import BeautifulSoup


def get_response(url, params={}, headers={}):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://engine.hotellook.com/api/v2/static"
TYPE2FILE = {
    "country": "/countries.json",
    "location": "/locations.json",
    "amenity": "/amenities/en.json"
}


def get_json_data(query, search_type, key, token=None):
    if key not in ("name", "code"):
        return {"error": "key should be either name or code."}
    try:
        response = get_response(
            BASE_URL + TYPE2FILE[search_type], {"token": token})
        for e in response:
            if type(e["name"]) == list:
                for name in e["name"]:
                    if "EN" in name:
                        e["name"] = name["EN"][0]["name"]
                        break
            if (key == "name" and e["name"] == query) \
                    or (key == "code" and e["code"] == query):
                return e
        if key == "name":
            return {"error": f"The input {query} may not be the name of any {search_type}."}
        else:
            return {"error": f"The input IATA code {query} may not correspond to any {search_type}."}
    except:
        return {"error": "Response error."}


def search_country(query: str, key: str = "name", token: str = ""):
    return get_json_data(query, "country", key, token)


def search_location(name: str, token: str = ""):
    return get_json_data(name, "location", "name", token)


def list_amenities(token: str = ""):
    response = get_response(BASE_URL + "/amenities/en.json", {"token": token})
    try:
        return [amenity["name"] for amenity in response]
    except:
        return response


def search_amenity(name: str, token: str = ""):
    return get_json_data(name, "amenity", "name", token)


def list_hotels(locationId: str, page: int = 0, page_size: int = 5,
                token: str = ""):
    params = {
        "locationId": locationId,
        "token": token
    }
    try:
        start = max(page * page_size, 0)
        end = max((page + 1) * page_size, start + 1)
        response = get_response(BASE_URL + "/hotels.json", params)
        return response["hotels"][start: end]
    except:
        return {"error": "Response error."}


def list_room_types(token: str = ""):
    return get_response(BASE_URL + "/roomTypes.json", {"token": token})


def list_hotel_types(token: str = ""):
    return get_response(BASE_URL + "/hotelTypes.json", {"token": token})


def hotel_photos(id: str):
    try:
        response = get_response(
            "https://yasen.hotellook.com/photos/hotel_photos", {"id": id})
        if type(response) == str:
            soup = BeautifulSoup(response, "html.parser")
            return {"error": soup.body.text}
        else:
            response["message"] = "You can view photos with these ids at https://photo.hotellook.com/image_v2/limit/photo_id/800/520.auto."
            return response
    except:
        return {"error": "Response error."}


def city_photo(city_iata: str, photo_size: Tuple[int, int] = (960, 720)):
    return f"https://photo.hotellook.com/static/cities/{photo_size[0]}x{photo_size[1]}/{city_iata}.jpg"


if __name__ == "__main__":
    # print(search_country("San Marino"))
    # print(search_location("Goa"))
    # print(list_amenities())
    # print(search_amenity("Chinese"))
    # print(list_hotels("895"))
    # print(list_room_types())
    # print(list_hotel_types())
    # print(hotel_photos("27926056,4"))
    print(city_photo("LED"))
