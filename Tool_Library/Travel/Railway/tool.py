import requests


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


def indian_railway_search(search: str, api_key: str = ""):
    payload = {"search": search}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "trains.p.rapidapi.com"
    }
    return post_response("https://trains.p.rapidapi.com/", payload, headers)


if __name__ == "__main__":
    print(indian_railway_search("Rajdhani"))
