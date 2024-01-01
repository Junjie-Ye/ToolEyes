import requests


def get_response(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def post_response(url, headers, params, data):
    response = requests.post(url, headers=headers, data=data, params=params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def timezone(
    api_key: enumerate = ""
):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }
    url = "https://api-formula-1.p.rapidapi.com/timezone"
    return get_response(url, headers)


def seasons(
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/seasons"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
    }

    return get_response(url=url, headers=headers, params=params)


def circuits(
    id: int = None,
    name: str = None,
    country: str = None,
    city: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/circuits"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "country": country,
        "city": city,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def competition(
    id: int = None,
    name: str = None,
    country: str = None,
    city: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/competitions"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "country": country,
        "city": city,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def drivers(
    id: int = None,
    name: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/drivers"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def races(
    id: int = None,
    date: str = None,
    next: int = None,
    last: int = None,
    competition: int = None,
    circuit: int = None,
    season: int = None,
    type: str = None,
    timezone: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/races"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "date": date,
        "next": next,
        "last": last,
        "competition": competition,
        "circuit": circuit,
        "season": season,
        "type": type,
        "timezone": timezone
    }

    return get_response(url=url, headers=headers, params=params)


def teams(
    id: int = None,
    name: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/teams"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def pit_stops(
    race: int,
    team: int = None,
    driver: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/pitstops"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "race": race,
        "team": team,
        "driver": driver
    }

    return get_response(url=url, headers=headers, params=params)


def rankings_drivers(
    season: int,
    driver: str = None,
    team: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/rankings/drivers"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "season": season,
        "driver": driver,
        "team": team
    }

    return get_response(url=url, headers=headers, params=params)


def rankings_races(
    race: int,
    driver: str = None,
    team: str = None,
    api_key: str = ""
):
    url = "https://api-formula-1.p.rapidapi.com/rankings/races"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-formula-1.p.rapidapi.com"
    }

    params = {
        "race": race,
        "driver": driver,
        "team": team
    }

    return get_response(url=url, headers=headers, params=params)


if __name__ == '__main__':
    # print(timezone())
    # print(seasons())
    # print(circuits(search="Australian"))
    # print(competition(id=1))
    # print(drivers(search="Lewi"))
    # print(races(date="2021-12-12", type="Race"))
    # print(teams(id=1))
    # print(pit_stops(race=50))
    # print(rankings_drivers(season=2021))
    print(rankings_races(race=50))
