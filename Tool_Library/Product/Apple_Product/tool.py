# from serpapi import GoogleSearch
import serpapi


def get_limited_list(array, length, limit, offset):
    if offset < 0:
        offset = 0
    if offset >= length or limit <= 0:
        return []
    if offset + limit > length:
        limit = length - offset
    return array[offset: offset + limit]


def apple_app_store_search(term: str, num: int = 2, page: int = 0, device: str = "mobile",
                           api_key: str = ""):
    params = {
        "engine": "apple_app_store",
        "api_key": api_key,
        "term": term,
        "num": num,
        "page": page,
        "device": device
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        return results["organic_results"]
    except:
        return results["error"]


def apple_product_search(product_id: str, type: str = "app",
                         api_key: str = "",
                         history: bool = False, also_like: bool = False, more_by_developer: bool = False):
    params = {
        "engine": "apple_product",
        "product_id": product_id,
        "type": type,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        del results["search_metadata"]
        del results["search_parameters"]
        del results["search_information"]
        # get reviews through apple_reviews_search()
        del results["ratings_and_reviews"]
        if not history:
            del results["version_history"]
        if not also_like:
            del results["you_may_also_like"]
        if not more_by_developer:
            del results["more_by_this_developer"]
        return results
    except:
        return results["error"]


def apple_reviews_search(product_id: str, page: int = 1, limit: int = 3, offset: int = 0, sort: str = "mostrecent",
                         api_key: str = ""):
    params = {
        "engine": "apple_reviews",
        "product_id": product_id,
        "page": page,
        "sort": sort,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        count = results["search_information"]["results_count"]
        return get_limited_list(results["reviews"], count, limit, offset)
    except:
        return results["error"]


if __name__ == "__main__":
    # print(apple_app_store_search("TestFlight"))
    # print(apple_product_search("534220544"))
    print(apple_reviews_search("534220544"))
