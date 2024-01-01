import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, params=kargs, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def series(api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = "https://cricket-live-data.p.rapidapi.com/series"
    return get_response(url, headers)


def fixtures(api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = "https://cricket-live-data.p.rapidapi.com/fixtures"
    return get_response(url, headers)


def fixtures_by_series(series_id: int, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = f"https://cricket-live-data.p.rapidapi.com/fixtures-by-series/{series_id}"
    return get_response(url, headers)


def fixtures_by_date(date: str, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = f"https://cricket-live-data.p.rapidapi.com/fixtures-by-date/{date}"

    return get_response(url, headers)


def results(api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = "https://cricket-live-data.p.rapidapi.com/results"
    return get_response(url, headers)


def results_by_date(date: str, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = f"https://cricket-live-data.p.rapidapi.com/results-by-date/{date}"
    return get_response(url, headers)


def match_scorecard(match_id: int, api_key: enumerate = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    url = f"https://cricket-live-data.p.rapidapi.com/match/{match_id}"
    return get_response(url, headers)


if __name__ == '__main__':
    # print(series())
    # print(fixtures())
    # print(fixtures_by_series(606))
    # print(fixtures_by_date("2020-09-21"))
    # print(results())
    # print(results_by_date("2020-09-20"))
    print(match_scorecard(2432999))
