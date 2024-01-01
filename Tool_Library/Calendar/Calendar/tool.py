import datetime
import calendar
import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def current_date():
    now = datetime.datetime.now()

    return f'Today is {calendar.day_name[now.weekday()]}, {calendar.month_name[now.month]} {now.day}, {now.year}.'


def available_countries():
    url = 'https://date.nager.at/api/v3/AvailableCountries'

    return get_response(url)


def country_info(countryCode: str):
    url = f'https://date.nager.at/api/v3/CountryInfo/{countryCode}'

    return get_response(url)


def long_weekend(year: int, countryCode: str):
    url = f'https://date.nager.at/api/v3/LongWeekend/{year}/{countryCode}'

    return get_response(url)


def public_holidays(year: int, countryCode: str):
    url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{countryCode}'

    return get_response(url)


def next_public_holidays(countryCode: str):
    url = f'https://date.nager.at/api/v3/NextPublicHolidays/{countryCode}'

    return get_response(url)


def next_public_holidays_worldwide():
    url = f'https://date.nager.at/api/v3/NextPublicHolidaysWorldwide'

    return get_response(url)


if __name__ == '__main__':
    print(current_date())
    print(next_public_holidays('CN'))
