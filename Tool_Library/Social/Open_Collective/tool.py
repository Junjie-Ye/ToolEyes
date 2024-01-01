import requests
from typing import Optional


def get_response(url, **kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    response = requests.get(url, kwargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://opencollective.com"


def get_collective_info(collectiveSlug: str):
    return get_response(BASE_URL + f"/{collectiveSlug}.json")


def get_members(collectiveSlug: str, memberType: str = "all", limit: int = 10, offset: int = 0):
    return get_response(BASE_URL + f"/{collectiveSlug}/members/{memberType}.json", limit=limit, offset=offset)


def get_members_per_tier(collectiveSlug: str, tierSlug: str, memberType: str = "all", limit: int = 10, offset: int = 0):
    return get_response(BASE_URL + f"/{collectiveSlug}/tiers/{tierSlug}/{memberType}.json", limit=limit, offset=offset)


def get_transactions(collectiveSlug: str, api_key: str, limit: int = 10, offset: int = 0,
                     type: Optional[str] = None, dateFrom: Optional[str] = None,
                     dateTo: Optional[str] = None, includeVirtualCards: bool = False):
    return get_response(BASE_URL + f"/v1/collectives/{collectiveSlug}/transactions",
                        api_key=api_key, limit=limit, offset=offset, type=type,
                        dateFrom=dateFrom, dateTo=dateTo, includeVirtualCards=includeVirtualCards)


def list_events(collectiveSlug: str, limit: int = 10, offset: int = 0):
    return get_response(BASE_URL + f"/{collectiveSlug}/events.json", limit=limit, offset=offset)


def get_event_info(collectiveSlug: str, eventSlug: str):
    return get_response(BASE_URL + f"/{collectiveSlug}/events/{eventSlug}.json")


def get_attendees_list(collectiveSlug: str, eventSlug: str, limit: int = 10, offset: int = 0):
    return get_response(BASE_URL + f"/{collectiveSlug}/events/{eventSlug}/attendees.json", limit=limit, offset=offset)


if __name__ == "__main__":
    # print(get_collective_info("webpack"))
    # print(get_members("webpack"))
    # print(get_members_per_tier("babel", "gold-sponsors"))
    # print(get_transactions("webpack", "YOUR_API_KEY"))
    # print(list_events("sustainoss"))
    # print(get_event_info("sustainoss", "2017-442ev"))
    print(get_attendees_list("sustainoss", "2017-442ev"))
