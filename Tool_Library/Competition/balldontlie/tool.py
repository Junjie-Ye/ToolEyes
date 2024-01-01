import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_all_players(page: int = 0, per_page: int = 25, search: str = None):
    url = 'https://www.balldontlie.io/api/v1/players'
    params = {'page': page, 'per_page': per_page, 'search': search}

    return get_response(url, **params)


def get_a_specific_player(player_id: int):
    url = f' https://www.balldontlie.io/api/v1/players/{player_id}'

    return get_response(url)


def get_all_teams(page: int = 0, per_page: int = 30):
    url = 'https://www.balldontlie.io/api/v1/teams'
    params = {'page': page, 'per_page': per_page}

    return get_response(url, **params)


def get_a_specific_team(team_id: int):
    url = f' https://www.balldontlie.io/api/v1/teams/{team_id}'

    return get_response(url)


def get_all_games(page: int = 0, per_page: int = 25, dates=None, seasons=None, team_ids=None, postseason: bool = None, start_date: str = None, end_date: str = None):
    url = 'https://www.balldontlie.io/api/v1/games'
    params = {'page': page, 'per_page': per_page, 'dates': dates, 'seasons': seasons,
              'team_ids': team_ids, 'postseason': postseason, 'start_date': start_date, 'end_date': end_date}

    return get_response(url, **params)


def get_a_specific_game(game_id: int):
    url = f' https://www.balldontlie.io/api/v1/games/{game_id}'

    return get_response(url)


def get_all_stats(page: int = 0, per_page: int = 25, dates=None, seasons=None, player_ids=None, game_ids=None, postseason: bool = None, start_date: str = None, end_date: str = None):
    url = 'https://www.balldontlie.io/api/v1/stats'
    params = {'page': page, 'per_page': per_page, 'dates': dates, 'seasons': seasons, 'player_ids': player_ids,
              'game_ids': game_ids, 'postseason': postseason, 'start_date': start_date, 'end_date': end_date}

    return get_response(url, **params)


def get_averages(season: str = 'current season', player_ids=None):
    url = ' https://www.balldontlie.io/api/v1/season_averages'
    params = {'season': season, 'player_ids': player_ids}

    return get_response(url, **params)


if __name__ == '__main__':
    print(get_all_players())
    print(get_a_specific_player(123))
    print(get_all_teams())
    print(get_a_specific_team(12))
    print(get_all_games())
    print(get_a_specific_game(12))
    print(get_all_stats())
    print(get_averages())
