import requests

# base url: https://api-football-v1.p.rapidapi.com/v3


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


def predictions(
    fixture: int,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "fixture": fixture
    }

    return get_response(url=url, headers=headers, params=params)


def fixtures_head_to_head(
    h2h: str,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "h2h": h2h
    }

    return get_response(url=url, headers=headers, params=params)


def fixtures(
    id: int = None,
    ids: str = None,
    live: str = None,
    date: str = None,
    league: int = None,
    season: str = None,
    team: int = None,
    last: int = None,
    next: int = None,
    from_date: str = None,
    to_date: str = None,
    round: str = None,
    timezone: str = None,
    status: str = None,
    venue: int = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "live": live,
        "date": date,
        "league": league,
        "season": season,
        "team": team,
        "last": last,
        "next": next,
        "from": from_date,
        "to": to_date,
        "round": round,
        "timezone": timezone,
        "status": status,
        "venue": venue,
        "ids": ids
    }

    return get_response(url=url, headers=headers, params=params)


def fixtures_round(
    league: int,
    season: int,
    current: bool = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "league": league,
        "season": season,
        "current": current
    }

    return get_response(url=url, headers=headers, params=params)


def teams_statistics(
    league: int,
    season: int,
    team: int,
    date: str = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "league": league,
        "season": season,
        "team": team,
        "date": date
    }

    return get_response(url=url, headers=headers, params=params)


def seasons(
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues/seasons"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
    }

    return get_response(url=url, headers=headers, params=params)


def countries(
    name: str = None,
    code: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/countries"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "name": name,
        "code": code,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def leagues(
    id: int = None,
    name: str = None,
    country: str = None,
    code: str = None,
    season: int = None,
    team: int = None,
    type: str = None,
    current: str = None,
    search: str = None,
    last: int = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "country": country,
        "code": code,
        "season": season,
        "team": team,
        "type": type,
        "current": current,
        "search": search,
        "last": last
    }

    return get_response(url=url, headers=headers, params=params)


def bets(
    id: int = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/odds/bets"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def bookmakers(
    id: int = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/odds/bookmakers"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def odds(
    fixture: int = None,
    league: int = None,
    season: int = None,
    date: str = None,
    timezone: str = None,
    page: int = 1,
    bookmaker: int = None,
    bet: int = None,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/odds"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "fixture": fixture,
        "league": league,
        "season": season,
        "date": date,
        "timezone": timezone,
        "page": page,
        "bookmaker": bookmaker,
        "bet": bet
    }

    return get_response(url=url, headers=headers, params=params)


def players(
    id: int = None,
    team: int = None,
    league: int = None,
    season: int = None,
    search: str = None,
    page: int = 1,
    api_key: str = ""
):
    url = "https://api-football-v1.p.rapidapi.com/v3/players"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "team": team,
        "league": league,
        "season": season,
        "search": search,
        "page": page
    }

    return get_response(url=url, headers=headers, params=params)


if __name__ == '__main__':
    # print(timezone())
    # print(predictions(198772))
    # print(fixtures(league=39, season=2020))
    # print(fixtures_round(league=39, season="2020"))
    # print(teams_statistics(league=39, season=2020, team=33))
    # print(teams_information(id=33))
    # print(seasons())
    # print(countries())
    # print(leagues(id=307, season=2020))
    # print(bets(id=307))
    # print(odds(league=10 ,season=2012))
    print(players(id=276, season=2020))
