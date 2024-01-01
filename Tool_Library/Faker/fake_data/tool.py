import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def fake_data(resource: str, _locale: str = "en_US", _quantity: int = 10, _seed: int = 123, **add_params):
    resource = resource.lower()
    _quantity = int(_quantity)
    _seed = int(_seed)
    if _quantity < 1:
        _quantity = 1
    url = f"https://fakerapi.it/api/v1/{resource}?_locale={_locale}&_quantity={_quantity}&_seed={_seed}"
    for key, value in add_params.items():
        url += f"&{key}={value}"
    # print(url)
    return get_response(url)


def fake_data_custom(custom_fields: dict, _locale: str = "en_US", _quantity: int = 10, _seed: int = None):
    _quantity = int(_quantity)
    _seed = int(_seed)
    if _quantity < 1:
        _quantity = 1
    if _seed == None:
        url = f"https://fakerapi.it/api/v1/custom?_locale={_locale}&_quantity={_quantity}"
    else:
        url = f"https://fakerapi.it/api/v1/custom?_locale={_locale}&_quantity={_quantity}&_seed={_seed}"
    for key, value in custom_fields.items():
        url += f"&{key}={value}"
    # print(url)
    return get_response(url)


if __name__ == "__main__":
    print(fake_data("images", _quantity=2, _type="architecture"))
    # print(fake_data_custom(custom_fields={"p":"pokemon"}))
