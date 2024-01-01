import requests


def get_response(url, params, headers):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


url = "https://text-similarity-calculator.p.rapidapi.com/stringcalculator.php"


def calculate_similarity(text1: str, text2: str, api_key: str = ""):
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "text-similarity-calculator.p.rapidapi.com"
    }

    params = {
        "ftext": text1,
        "stext": text2
    }

    return get_response(url, params, headers)


if __name__ == "__main__":
    print(calculate_similarity("This is text numer one.", "This is text number two."))
