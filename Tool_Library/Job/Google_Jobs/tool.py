# from serpapi import GoogleSearch
from typing import Optional
import serpapi


def google_jobs_search(query: str, gl: Optional[str] = None, api_key: str = ""):
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": api_key,
        "gl": gl,
        "hl": "en",
        "output": "json"
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    try:
        return results["jobs_results"]
    except:
        return results["error"]


def google_jobs_listing_search(job_id: str, api_key: str = ""):
    params = {
        "engine": "google_jobs_listing",
        "q": job_id,
        "api_key": api_key
    }

    # search = GoogleSearch(params)
    # results = search.get_dict()
    results = serpapi.search(**params)
    return results


if __name__ == "__main__":
    print(google_jobs_search("barista new york"))
    print(google_jobs_listing_search("eyJqb2JfdGl0bGUiOiJCYXJpc3RhIiwiaHRpZG9jaWQiOiJMV1J1RlY4ZHZka0FBQUFBQUFBQUFBPT0iLCJobCI6ImVuIiwiZmMiOiJFdmNCQ3JjQlFVMXJNbXhzU1c0NFUweEtZVGhJV1RsZlkwZEtUa2hVU0RsSlRWUTBWazQyUlZCUE5UTXdURzF1V1dkalYzazJjMU5WVXpGUExWTnRlWGQzTkRWWE1uazViMVl5YjFGcmQzcHljbkoxY2pGeU4zSlBkVGg2TTJock1tTlhlbWxxVm5OTFJVTkhaV2hDVjFWTFYycFRVVUp1ZDFCU1ozZFRaRzFFVGpCRWFHZG1PRk14V2xaNWIzUnVjV1p4ZVVabmNUVkVkMlZXZFhvNGIzQm9abXB1ZEZKVWNXRTVkMFJpVXpsaU56WmhaVjlwVVRGc1ZYbzRFaGRxTFdKWVdrcFFVVXBaYVZkM1ltdFFYemhsT1hOQmF4b2lRVXhGVXpsMVR6Qm9hWGRRUVZsMUxWaENhR3htTm5GV1RVVk1NalJaVkZNM1VRIiwiZmN2IjoiMyIsImZjX2lkIjoiZmNfMSIsImFwcGx5X2xpbmsiOnsidGl0bGUiOiIubkZnMmVie2ZvbnQtd2VpZ2h0OjUwMH0uQmk2RGRje2ZvbnQtd2VpZ2h0OjUwMH1BcHBseSBkaXJlY3RseSBvbiBJbmRlZWQiLCJsaW5rIjoiaHR0cHM6Ly93d3cuaW5kZWVkLmNvbS92aWV3am9iP2prPTk4MTdkOWMzMGUzNjEzZWJcdTAwMjZ1dG1fY2FtcGFpZ249Z29vZ2xlX2pvYnNfYXBwbHlcdTAwMjZ1dG1fc291cmNlPWdvb2dsZV9qb2JzX2FwcGx5XHUwMDI2dXRtX21lZGl1bT1vcmdhbmljIn19"))
