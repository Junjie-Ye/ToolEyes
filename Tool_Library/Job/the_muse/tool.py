import requests
from typing import Optional, Union, List


def get_response(url, params={}):
    response = requests.get(url, params)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://www.themuse.com/api/public"


def search_jobs(page: int = 0, descending: Optional[bool] = False, company: Optional[Union[str, List[str]]] = None,
                category: Optional[str] = None, level: Optional[str] = None, location: Optional[str] = None):
    params = {
        "page": page,
        "descending": descending,
        "company": company,
        "category": category,
        "level": level,
        "location": location
    }
    params = {k: v for k, v in params.items() if v is not None}
    return get_response(BASE_URL + "/jobs", params)


def search_job_by_id(job_id: str):
    return get_response(BASE_URL + f"/jobs/{job_id}")


def search_companies(page: int = 0, descending: Optional[bool] = False,
                     industry: Optional[str] = None, size: Optional[str] = None,
                     location: Optional[str] = None):
    params = {
        "page": page,
        "descending": descending,
        "industry": industry,
        "size": size,
        "location": location
    }
    params = {k: v for k, v in params.items() if v is not None}
    return get_response(BASE_URL + "/companies", params)


def search_company_by_id(company_id: str):
    return get_response(BASE_URL + f"/companies/{company_id}")


if __name__ == "__main__":
    # print(search_jobs())
    # print(search_job_by_id("11404163"))
    # print(search_companies())
    print(search_company_by_id("15000118"))
