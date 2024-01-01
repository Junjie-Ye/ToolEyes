import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def common_refine_func(season: str = None, race: int = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None, driver_standings: int = None, constructor_standings: int = None):
    url = f' http://ergast.com/api/f1/'
    if season is not None:
        url += f'{season}/'
    if race is not None:
        url += f'{race}/'
    if circuit_id is not None:
        url += f'circuits/{circuit_id}/'
    if constructor_id is not None:
        url += f'constructors/{constructor_id}/'
    if driver_id is not None:
        url += f'drivers/{driver_id}/'
    if grid_position is not None:
        url += f'grid/{grid_position}/'
    if results_position is not None:
        url += f'results/{results_position}/'
    if rank is not None:
        url += f'fastest/{rank}/'
    if status_id is not None:
        url += f'status/{status_id}/'
    if driver_standings is not None:
        url += f'driverStandings/{driver_standings}/'
    if constructor_standings is not None:
        url += f'constructorStandings/{constructor_standings}/'
    return (url)


def season_list(season: str = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None, driver_standings: int = None, constructor_standings: int = None):
    url = common_refine_func(season, circuit_id, constructor_id, driver_id, grid_position,
                             results_position, rank, status_id, driver_standings, constructor_standings)
    url += 'seasons'
    url += '.json'

    return get_response(url)


def qualifying_results(season: str = None, race: int = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None, finishing_position: int = None):
    url = common_refine_func(season, race, circuit_id, constructor_id,
                             driver_id, grid_position, results_position, rank, status_id)
    url += 'qualifying'
    if finishing_position is not None:
        url += f'/{finishing_position}'
    url += '.json'

    return get_response(url)


def constructor_information(season: str = None, race: int = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None):
    if constructor_id is not None:
        url = f"http://ergast.com/api/f1/constructors/{constructor_id}"
    else:
        url = common_refine_func(season, race, circuit_id, constructor_id,
                                 driver_id, grid_position, results_position, rank, status_id)
        url += 'constructors'
    url += '.json'

    return get_response(url)


def lap_times(season: str, round: int, lap_number: int, driver_id: str = None):
    if driver_id is not None:
        url = f'http://ergast.com/api/f1/{season}/{round}/drivers/{driver_id}/laps/{lap_number}'
    else:
        url = f'http://ergast.com/api/f1/{season}/{round}/laps/{lap_number}'
    url += '.json'

    return get_response(url)


def race_schedule(season: str = None, race: int = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None):
    url = common_refine_func(season, race, circuit_id, constructor_id,
                             driver_id, grid_position, results_position, rank, status_id)
    url += 'races'
    url += '.json'

    return get_response(url)


def driver_standings(season: str = None, race: int = None, driver_id: str = None, driver_standings: int = None):
    if driver_standings is not None:
        url = f"http://ergast.com/api/f1/driverStandings/{driver_standings}"
    else:
        url = common_refine_func(season=season, race=race, driver_id=driver_id)
        url += "driverStandings"
    url += '.json'

    return get_response(url)


def constructor_Standings(season: str = None, race: int = None, constructor_id: str = None, constructor_standings: int = None):
    if constructor_standings is not None:
        url = f"http://ergast.com/api/f1/constructorStandings/{constructor_standings}"
    else:
        url = common_refine_func(
            season=season, race=race, constructor_id=constructor_id)
        url += "constructorStandings"
    url += '.json'

    return get_response(url)


def circuit_information(season: str = None, race: int = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None):
    if circuit_id is not None:
        url = f"http://ergast.com/api/f1/circuits/{circuit_id}"
    else:
        url = common_refine_func(season, race, circuit_id, constructor_id,
                                 driver_id, grid_position, results_position, rank, status_id)
        url += 'circuits'
    url += '.json'

    return get_response(url)


def pit_stops(season: str, race=int, stop_number: int = None, driver_id: str = None, lap_number: int = None):
    url = common_refine_func(season=season, race=race, driver_id=driver_id)
    if lap_number is not None:
        url += f'laps/{lap_number}'
    if stop_number is not None:
        url += f'pitstops/{stop_number}'
    else:
        url += 'pitstops'
    url += '.json'
    # print(url)

    return get_response(url)


def race_results(season: str, race: str, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, rank: int = None, status_id: int = None, finishing_position: int = None):
    url = common_refine_func(season=season, race=race, circuit_id=circuit_id, constructor_id=constructor_id,
                             driver_id=driver_id, grid_position=grid_position, rank=rank, status_id=status_id)
    url += 'results'
    if finishing_position is not None:
        url += f'/{finishing_position}'
    url += '.json'

    return get_response(url)


def driver_information(season: str = None, race: str = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None, driver_standings: int = None,):
    url = common_refine_func(season=season, race=race, circuit_id=circuit_id, constructor_id=constructor_id, driver_id=driver_id,
                             grid_position=grid_position, results_position=results_position, rank=rank, status_id=status_id, driver_standings=driver_standings)
    url += "drivers.json"

    return get_response(url)


def finishing_status(season: str = None, race: str = None, circuit_id: str = None, constructor_id: str = None, driver_id: str = None, grid_position: int = None, results_position: int = None, rank: int = None, status_id: int = None,):
    url = common_refine_func(season=season, race=race, circuit_id=circuit_id, constructor_id=constructor_id,
                             driver_id=driver_id, grid_position=grid_position, results_position=results_position, rank=rank, status_id=status_id)
    url += "status.json"

    return get_response(url)


if __name__ == '__main__':
    # print(season_list(driver_id="alonso",constructor_id="renault"))
    # print(qualifying_results(driver_id="alonso",constructor_id="renault"))
    # print(constructor_information(driver_id="alonso",circuit_id="monza"))
    # print(lap_times("2011",5,1,driver_id="alonso"))
    # print(race_schedule(driver_id="alonso",circuit_id="monza"))
    # print(driver_standings(driver_id="alonso"))
    # print(constructor_standings(constructor_id="renault"))
    # print(constructor_standings(constructor_standings=1))
    print(circuit_information(circuit_id="monza"))
    # print(pit_stops("2011",5,driver_id="alonso"))
    # print(race_results(season="2008",driver_id="alonso"))
    # print(driver_information(constructor_id="mclaren",circuit_id="monza"))
    # print(finishing_status(season="2008",driver_id="alonso"))
