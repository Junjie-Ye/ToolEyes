import requests
from typing import Optional, Union, List


def get_response(url, params, headers):
    response = requests.get(url, params, headers=headers)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://jsearch.p.rapidapi.com"
API_HOST = "jsearch.p.rapidapi.com"


def basic_job_search(query: str, page: int = 1, num_pages: str = "1", date_posted: Optional[str] = None,
                     remote_jobs_only: Optional[bool] = None, employment_types: Optional[str] = None,
                     job_requirements: Optional[str] = None, job_titles: Optional[str] = None,
                     company_types: Optional[str] = None, employer: Optional[str] = None,
                     radius: Optional[int] = None,
                     api_key: str = "") -> dict:
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }
    querystring = {
        "query": query,
        "page": page,
        "num_pages": num_pages
    }
    if date_posted:
        querystring['date_posted'] = date_posted
    if remote_jobs_only is not None:
        querystring['remote_jobs_only'] = remote_jobs_only
    if employment_types:
        querystring['employment_types'] = employment_types
    if job_requirements:
        querystring['job_requirements'] = job_requirements
    if job_titles:
        querystring['job_titles'] = job_titles
    if company_types:
        querystring['company_types'] = company_types
    if employer:
        querystring['employer'] = employer
    if radius:
        querystring['radius'] = radius

    response = get_response(BASE_URL + "/search", querystring, headers)
    try:
        return response["data"]
    except:
        return response


def search_jobs_with_filters(query: str, page: int = 1, num_pages: int = 1, date_posted: str = "all",
                             remote_jobs_only: bool = False, employment_types: Optional[str] = None,
                             job_requirements: Optional[str] = None, job_titles: Optional[str] = None,
                             company_types: Optional[str] = None, employer: Optional[str] = None,
                             radius: Optional[int] = None, categories: Optional[str] = None,
                             api_key: str = "") -> dict:
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }
    params = {
        "query": query,
        "page": str(page),
        "num_pages": str(num_pages),
        "date_posted": date_posted,
        "remote_jobs_only": str(remote_jobs_only).lower(),
        "employment_types": employment_types,
        "job_requirements": job_requirements,
        "job_titles": job_titles,
        "company_types": company_types,
        "employer": employer,
        "radius": str(radius) if radius else None,
        "categories": categories
    }

    # remove None values in the parameters
    params = {k: v for k, v in params.items() if v is not None}

    response = get_response(BASE_URL + "/search-filters",
                            params, headers=headers)
    try:
        return response["data"]
    except:
        return response


def get_job_details(job_ids: Union[str, List[str]], extended_publisher_details: bool = False,
                    api_key: str = "") -> dict:
    if isinstance(job_ids, list):
        job_ids = ','.join(job_ids)
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }
    querystring = {
        "job_id": job_ids,
        "extended_publisher_details": str(extended_publisher_details).lower()
    }
    response = get_response(BASE_URL + "/job-details", querystring, headers)
    try:
        return response["data"]
    except:
        return response


def get_salary_estimation(job_title: str, location: str, radius: int = 200,
                          api_key: str = "") -> dict:
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": API_HOST
    }
    querystring = {}
    if job_title:
        querystring['job_title'] = job_title
    if location:
        querystring['location'] = location
    if radius:
        querystring['radius'] = radius
    response: dict = get_response(
        BASE_URL + "/estimated-salary", querystring, headers)
    try:
        return response["data"]
    except:
        return response


if __name__ == "__main__":
    # print(basic_job_search("Python developer in Texas, USA"))
    # print(search_jobs_with_filters("Python developer in Texas, USA"))
    # print(get_job_details("fFunVwyb9l4AAAAAAAAAAA=="))
    print(get_salary_estimation("NodeJS Developer", "New-York, NY, USA", 100))
