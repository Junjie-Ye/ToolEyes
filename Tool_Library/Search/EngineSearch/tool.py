import requests
import serpapi
# There is no avaliable pachage for serpapi at pypi, please download and install it at https://github.com/serpapi/serpapi-python.git


def get_default_key():
    api_key = ""
    return api_key


def get_search_results(engine, **kwargs):
    engine = engine.lower().strip()
    params = {
        "engine": engine,
        "output": 'JSON'
    }
    for arg_name, arg_value in kwargs.items():
        params[arg_name] = arg_value
    results = serpapi.search(**params)
    return results


def get_further_contents(request_url):
    results = requests.get(request_url)
    return results.text


def google_autocomplete_search(query, api_key=None, **kwargs):
    engine = 'google_autocomplete'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['suggestions']


def google_related_question_search(query, api_key=None, **kwargs):
    engine = 'google'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['related_searches']


def baidu_search(query, api_key=None, **kwargs):
    engine = 'baidu'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def google_search(query, api_key=None, **kwargs):
    engine = 'google'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def bing_search(query, api_key=None, **kwargs):
    engine = 'bing'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def duckduckgo_search(query, api_key=None, **kwargs):
    engine = 'duckduckgo'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def naver_search(query, api_key=None, **kwargs):
    engine = 'naver'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, query=query, api_key=api_key, **kwargs)
    return results['view_results']


def yahoo_search(query, api_key=None, **kwargs):
    engine = 'yahoo'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, p=query, api_key=api_key, **kwargs)
    return results['organic_results']


def yelp_search(query, find_loc="San Francisco, CA 94103", api_key=None, **kwargs):
    engine = 'yelp'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, find_desc=query, find_loc=find_loc, api_key=api_key, **kwargs)
    return results['organic_results']


def bing_news_search(query, api_key=None, **kwargs):
    engine = 'bing_news'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def baidu_news_search(query, api_key=None, **kwargs):
    engine = 'baidu_news'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


if __name__ == '__main__':
    query = '今天午饭吃什么'
    api_key = ""
    print(baidu_news_search(query))
