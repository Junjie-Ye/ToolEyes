# from serpapi import GoogleSearch
from typing import Optional, Union, List
import serpapi


def get_limited_list(array, length, limit, offset):
    if offset < 0:
        offset = 0
    if offset >= length or limit <= 0:
        return []
    if offset + limit > length:
        limit = length - offset
    return array[offset: offset + limit]


def google_trends_search(query: Union[str, List[str]], geo: Optional[str] = None, region: Optional[str] = None,
                         data_type: str = "TIMESERIES", tz: int = 420, cat: int = 0, gprop: Optional[str] = None,
                         date: str = "now 1-d", api_key: str = "",
                         limit: int = 5, offset: int = 0):
    if isinstance(query, list):
        query = ",".join(query)
    params = {
        "engine": "google_trends",
        "q": query,
        "geo": geo,
        "region": region,
        "data_type": data_type,
        "tz": tz,
        "cat": cat,
        "gprop": gprop,
        "date": date,
        "api_key": api_key,
    }
    params = {k: v for k, v in params.items() if v is not None}

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    if "error" in results.keys():
        return results["error"]
    response = []
    if data_type == "GEO_MAP":
        response = results["compared_breakdown_by_region"]
    elif data_type == "GEO_MAP_0":
        response = results["interest_by_region"]
    elif data_type == "TIMESERIES":
        response = results["interest_over_time"]["timeline_data"]
    elif data_type == "RELATED_QUERIES":
        response = results["related_queries"]["rising"]
    elif data_type == "RELATED_TOPICS":
        response = results["related_topics"]["rising"]
    return get_limited_list(response, len(response), limit, offset)


def google_trends_autocomplete_search(query: str, api_key: str = ""):
    params = {
        "engine": "google_trends_autocomplete",
        "q": query,
        "api_key": api_key
    }
    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        return results["suggestions"]
    except:
        return results["error"]


if __name__ == "__main__":
    # print(google_trends_search(["coffee", "milk", "bread", "pasta", "steak"], data_type="GEO_MAP"))
    # print(google_trends_search("coffee", data_type="GEO_MAP_0")),
    # print(google_trends_search(["coffee", "milk", "bread", "pasta", "steak"], data_type="TIMESERIES"))
    # print(google_trends_search("coffee", data_type="RELATED_QUERIES"))
    # print(google_trends_search("coffee", data_type="RELATED_TOPICS"))
    print(google_trends_autocomplete_search("Stripe"))
