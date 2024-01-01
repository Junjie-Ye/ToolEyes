import requests

# https://rapidapi.com/ortegalex/api/horse-racing

base_url = "https://horse-racing.p.rapidapi.com/"


def get_response(url, headers, **kargs):
    response = requests.get(url, params=kargs, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def race_detail_info(id_race: int, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    url = base_url + f"race/{id_race}"
    response = get_response(url, headers=headers)

    return (response)


def racecards(date: str = None, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    url = base_url + "racecards"
    querystring = {"date": date}
    response = get_response(url, headers=headers, params=querystring)

    return (response)


def results(date: str = None, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    url = base_url + "results"
    querystring = {"date": date}
    response = get_response(url, headers=headers, params=querystring)

    return (response)


def horse_stats(id_horse: int, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    url = base_url + f"horse-stats/{id_horse}"
    response = get_response(url, headers=headers)

    return (response)


def jockeys_win_rate(last_days: int = 7, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    params = {"last_days": last_days}
    url = base_url + "jockeys-win-rate"
    response = get_response(url, headers=headers, **params)

    return (response)


def trainers_win_rate(last_days: int = 7, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    params = {"last_days": last_days}
    url = base_url + "trainers-win-rate"
    response = get_response(url, headers=headers, **params)

    return (response)


def query_races(api_key: enumerate = "", course: str = None, name: str = None, distance_from: enumerate = None, distance_to: enumerate = None, class_from: int = None, class_to: int = None, id_horse: int = None, date_from: str = None, date_to: str = None, page: int = None, order_by_date: enumerate = None):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    params = {"course": course, "name": name, "distance_from": distance_from, "distance_to": distance_to, "class_from": class_from,
              "class_to": class_to, "id_horse": id_horse, "date_from": date_from, "date_to": date_to, "page": page, "order_by_date": order_by_date}
    url = base_url + "query-races"
    response = get_response(url, headers=headers, **params)

    return (response)


def query_horses(name: str, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"
    }
    params = {"name": name}
    url = base_url + "query-horses"
    response = get_response(url, headers=headers, **params)

    return (response)


if __name__ == '__main__':
    # print(race_detail_info(207660))
    # print(racecards("2020-01-01"))
    # print(results("2020-03-13"))
    # print(horse_stats("230380"))
    # print(jockeys_win_rate())
    # print(trainers_win_rate())
    # print(query_races())
    print(query_horses(name="ZANAHIYR"))

    # pass
