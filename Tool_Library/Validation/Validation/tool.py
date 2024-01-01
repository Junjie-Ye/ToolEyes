import requests
# import detectlanguage


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def profanity_detect(text: str):
    url = 'https://www.purgomalum.com/service/json?text={}'.format(text)
    return get_response(url)


def check_phone_number(number, api_key='', country_code='CN'):
    url = 'http://apilayer.net/api/validate?access_key={}&number={}&country_code={}'.format(
        api_key, number, country_code)
    return get_response(url)


def analyze_scan(website: str):
    url = "https://http-observatory.security.mozilla.org/api/v1/analyze?host={}".format(
        website)
    return get_response(url)


def get_scan_results(id):
    url = "https://http-observatory.security.mozilla.org/api/v1/getScanResults?scan={}".format(
        id)
    return get_response(url)


def get_recent_scans(way, score):
    url = "https://http-observatory.security.mozilla.org/api/v1/getRecentScans?{}={}".format(
        way, score)
    return get_response(url)


def get_host_history(host_name: str):
    url = "https://http-observatory.security.mozilla.org/api/v1/getHostHistory?host={}".format(
        host_name)
    return get_response(url)


def get_grade_distribution():
    url = "https://http-observatory.security.mozilla.org/api/v1/getGradeDistribution"
    return get_response(url)


if __name__ == '__main__':
    # print(profanity_detect("fuck you son of the bitch"))
    # print(check_phone_number(123456789))
    # print(get_scan_results(123456))
    # print(get_recent_scans(way='min',score='20'))
    # print(get_grade_distribution())
    pass
