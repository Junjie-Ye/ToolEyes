import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_daily_calory_requirement(
    age: int,
    gender: str,
    height: int,
    weight: int,
    activitylevel: str,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    params = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activitylevel": activitylevel,
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }
    return get_response(url, headers, **params)


def get_calories_burned(
    activityid: str,
    activitymin: int,
    weight: int,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/burnedcalorie"

    params = {"activityid": activityid,
              "activitymin": activitymin, "weight": weight}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }
    return get_response(url, headers, **params)


def get_bmi(
    age: int,
    height: int,
    weight: int,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/bmi"

    params = {"age": age, "weight": weight, "height": height}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_macro_nutrients_amount(
    age: int,
    gender: str,
    height: int,
    weight: int,
    activitylevel: int,
    goal: str,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/macrocalculator"

    params = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activitylevel": activitylevel,
        "goal": goal,
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_body_fat_percentage(
    age: int,
    gender: str,
    height: int,
    weight: int,
    neck: int,
    waist: int,
    hip: int,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/bodyfat"

    params = {
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "neck": neck,
        "waist": waist,
        "hip": hip,
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_ideal_weight(
    gender: str,
    height: int,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/idealweight"

    params = {"gender": gender, "height": height}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_food_info(
    foodid: str,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/food"

    params = {"foodid": foodid}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_foodtable_ids(
    subtablename: str = "Fo1_2",
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/foodids"

    params = {"subtablename": subtablename}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_subtable_names(
    tablename: str,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/foodids/subtablenames"

    params = {"tablename": tablename}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_maintable_names(
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/foodids/tablenames"

    params = {}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


def get_acitcity_met_values(
    activitylevel: int,
    api_key: str = "",
):
    url = "https://fitness-calculator.p.rapidapi.com/activities"
    params = {"intensitylevel": activitylevel}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com",
    }

    return get_response(url, headers, **params)


if __name__ == "__main__":
    # print(get_daily_calory_requirement(25, "male", 180, 70, "level_1"))
    # print(get_calories_burned("bi_1", 25, 75))
    # print(get_bmi(25, 180,75))
    # print(get_macro_nutrients_amount(25, "male", 180, 70, 5, "extremelose"))
    # print(get_body_fat_percentage(25, "male", 178, 70, 50, 96, 92))
    # print(get_ideal_weight("male", 180))
    # print(get_food_info("SR25_1_1"))
    # print(get_foodtable_ids("Fo1_2"))
    # print(get_subtable_names("Su10"))
    # print(get_maintable_names())
    # print(get_acitcity_met_values(1))
    pass
