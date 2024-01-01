# from serpapi import GoogleSearch
from typing import Optional
import serpapi


def get_limited_list(array, length, limit, offset):
    if offset < 0:
        offset = 0
    if offset >= length or limit <= 0:
        return []
    if offset + limit > length:
        limit = length - offset
    return array[offset: offset + limit]


def walmart_search(query: str, sort: Optional[str] = None, grid: bool = True,
                   store_id: Optional[str] = None, min_price: Optional[int] = None, max_price: Optional[int] = None,
                   nd_en: bool = False, page: int = 1, limit: int = 5, offset: int = 0, device: str = "desktop",
                   api_key: str = ""):
    params = {
        "engine": "walmart",
        "query": query,
        "api_key": api_key,
        "page": page,
        "ps": 40,
        "sort": sort,
        "grid": grid,
        "store_id": store_id,
        "min_price": min_price,
        "max_price": max_price,
        "nd_en": nd_en,
        "device": device,
    }
    params = {k: v for k, v in params.items() if v is not None}

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        organic_results = results["organic_results"]
        return get_limited_list(organic_results, len(organic_results), limit, offset)
    except:
        return results["error"]


if __name__ == "__main__":
    print(walmart_search("Coffee"))
