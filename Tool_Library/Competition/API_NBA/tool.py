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


def seasons(
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/seasons"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
    }

    return get_response(url=url, headers=headers, params=params)


def leagues(
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/leagues"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
    }

    return get_response(url=url, headers=headers, params=params)


def games(
    id: int = None,
    date: str = None,
    live: str = None,
    league: int = None,
    season: int = None,
    team: int = None,
    h2h: str = None,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/games"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "date": date,
        "live": live,
        "league": league,
        "season": season,
        "team": team,
        "h2h": h2h
    }

    return get_response(url=url, headers=headers, params=params)


def game_statistics(
    id: int,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/games/statistics"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
    }

    return get_response(url=url, headers=headers, params=params)


def teams(
    id: int = None,
    name: str = None,
    code: str = None,
    league: int = None,
    conference: str = None,
    division: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/teams"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "code": code,
        "league": league,
        "conference": conference,
        "division": division,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def team_statistics(
    id: int,
    season: str,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/teams/statistics"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "season": season
    }

    return get_response(url=url, headers=headers, params=params)


def players(
    id: int = None,
    name: str = None,
    team: int = None,
    season: int = None,
    country: str = None,
    search: str = None,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/players"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "name": name,
        "team": team,
        "season": season,
        "country": country,
        "search": search
    }

    return get_response(url=url, headers=headers, params=params)


def player_statistics(
    id: int = None,
    game: int = None,
    team: int = None,
    season: int = None,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "id": id,
        "game": game,
        "team": team,
        "season": season,
    }

    return get_response(url=url, headers=headers, params=params)


def standings(
    league: str,
    season: int,
    team: int = None,
    conference: str = None,
    division: str = None,
    api_key: str = ""
):
    url = "https://api-nba-v1.p.rapidapi.com/standings"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    params = {
        "league": league,
        "season": season,
        "team": team,
        "conference": conference,
        "division": division
    }

    return get_response(url=url, headers=headers, params=params)


if __name__ == '__main__':
    # print(seasons())
    # print(games(season=2020))
    # print(game_statistics(id=10403))
    # print(teams(name="Lakers"))
    # print(team_statistics(id=14, season=2020))
    # print(players(team=1, season=2020))
    # print(player_statistics(id=236, season=2020))
    print(standings(league="standard", season=2021))
