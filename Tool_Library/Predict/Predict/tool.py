import requests
from typing import Optional, Union, List


def get_response(url, params):
    response = requests.get(url, params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def predict_age(names: Union[str, List[str]], country_id: Optional[str] = None):
    if not isinstance(names, list):
        names = [names]
    params = {"name[]": names}
    if country_id is not None:
        params["country_id"] = country_id
    return get_response("https://api.agify.io", params)


def predict_gender(names: Union[str, List[str]], country_id: Optional[str] = None):
    if not isinstance(names, list):
        names = [names]
    params = {"name[]": names}
    if country_id is not None:
        params["country_id"] = country_id
    return get_response("https://api.genderize.io", params)


def predict_nationality(names: Union[str, List[str]]):
    if not isinstance(names, list):
        names = [names]
    params = {"name[]": names}
    return get_response("https://api.nationalize.io", params)


if __name__ == "__main__":
    # print(predict_age(["jane", "michael"], "US"))
    # print(predict_gender(["alice", "bob"], "CA"))
    print(predict_nationality(["jane", "michael"]))
