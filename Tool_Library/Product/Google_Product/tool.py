# from serpapi import GoogleSearch
from typing import Optional
import serpapi


def google_immersive_product_search(page_token: str, api_key: str = ""):
    params = {
        "engine": "google_immersive_product",
        "page_token": page_token,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        return {
            "product_results": results["product_results"],
            "similar_products": results["similar_products"]
        }
    except:
        return results["error"]


def google_shopping_search(query: str, start: int = 0, num: int = 3, device: str = "desktop",
                           api_key: str = ""):
    start = int(start)
    num = int(num)
    if num < 1:
        num = 3
    params = {
        "engine": "google_shopping",
        "q": query,
        "start": start,
        "num": num,
        "device": device,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        return results["shopping_results"]
    except:
        return results["error"]


def google_product_search(product_id: str, start: int = 0, offers: bool = False, specs: bool = False, reviews: bool = False,
                          device: str = "desktop", api_key: str = ""):
    start = int(start)
    params = {
        "engine": "google_product",
        "product_id": product_id,
        "start": start,
        "device": device,
        "api_key": api_key
    }
    if offers:
        params["offers"] = "1"
    elif specs:
        params["specs"] = "1"
    elif reviews:
        params["reviews"] = "1"

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        res = {"product_results": results["product_results"]}
        if offers:
            res["sellers_results"] = results["sellers_results"]
        if specs:
            res["specs_results"] = results["specs_results"]
        if reviews:
            res["reviews_results"] = results["reviews_results"]
        return res
    except:
        return results["error"]


if __name__ == "__main__":
    # print(google_immersive_product_search("eyJlaSI6IlN3clNZcmFlRnFETXdia1A0Y20zMkFvIiwiY2F0YWxvZ2lkIjoiMTU5NTU5MzkxODU0NTAwMDU3MjUiLCJ2YyI6IjI1OTQ0NzAwMTQxODE5NDE0ODgiLCJ2c2MiOiI2NjYyMzE2OTMzMjUwMjk2MDcwIiwiaGVhZGxpbmVPZmZlckRvY2lkIjoiMTMxOTk2NzY4MTI5MDY4NTQ5MDEiLCJpbWFnZURvY2lkIjoiMTgwMDcyMTg2NzgwOTA4Nzg3OTUiLCJyZHMiOiJQQ182MDUyMTgzNjI1MTU3Mzc5NjAxfFBST0RfUENfNjA1MjE4MzYyNTE1NzM3OTYwMSIsInF1ZXJ5IjoibWVucytzd2VhdGVyIn0="))
    # print(google_shopping_search("Macbook M2"))
    print(google_product_search("4172129135583325756"))
