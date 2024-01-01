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
    try:
        return results.content
    except:
        return results


def bing_image_search(query, api_key=None, **kwargs):
    engine = 'bing_images'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['images_results']


def yahoo_image_search(query, api_key=None, **kwargs):
    engine = 'yahoo_images'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, p=query, api_key=api_key, **kwargs)
    return results['images_results']


def yandex_videos_search(query, api_key=None, **kwargs):
    engine = 'yandex_videos'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(engine, text=query, api_key=api_key, **kwargs)
    return results['videos_results']


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


def youtube_search(query, api_key=None, **kwargs):
    engine = 'youtube'
    if not api_key:
        api_key = get_default_key()
    results = get_search_results(
        engine, search_query=query, api_key=api_key, **kwargs)
    return results['channel_results']


if __name__ == '__main__':
    query = 'miaomiao'
    api_key = ""
    print(yahoo_image_search(query))
