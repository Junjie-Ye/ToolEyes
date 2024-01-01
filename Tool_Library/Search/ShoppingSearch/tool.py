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
    return results.content


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


def bing_shopping_search(query, api_key=None, **kwargs):
    engine = 'bing_shopping'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['shopping_results']


def ebay_search(query, api_key=None, **kwargs):
    engine = 'ebay'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, _nkw=query, api_key=api_key, **kwargs)
    return results['organic_results']


def yahoo_shopping_search(query, api_key=None, **kwargs):
    engine = 'yahoo_shopping'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, p=query, api_key=api_key, **kwargs)
    try:
        return results['shopping_results']
    except KeyError:
        return "Yahoo Shopping hasn't returned any results for this query."


def walmart_search(query, api_key=None, **kwargs):
    engine = 'walmart'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, query=query, api_key=api_key, **kwargs)
    try:
        return results['organic_results']
    except KeyError:
        return "The product could not be found."


def walmart_review_search(query, api_key=None, **kwargs):
    engine = 'walmart_product'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, product_id=query, api_key=api_key, **kwargs)
    return results['reviews_results']


def yelp_reviews_search(query, api_key=None, **kwargs):
    engine = 'yelp_reviews'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, place_id=query, api_key=api_key, **kwargs)
    return results['reviews']


if __name__ == '__main__':
    query = '520468661'
    api_key = ""
    print(walmart_search(query))
