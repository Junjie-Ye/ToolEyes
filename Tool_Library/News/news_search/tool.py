import requests


def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_news_everything(api_key="", q=None, searchIn="title,description", sources=None, domains=None, excludeDomains=None, from_date="2023-08-13", to_date="2023-08-13", language="en", sortBy="publishedAt", pageSize=2, page=1):
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "searchIn": searchIn,
        "from": from_date,
        "to": to_date,
        "language": language,
        "sortBy": sortBy,
        "pageSize": pageSize,
        "page": page
    }

    if q:
        params["q"] = q
    if sources:
        params["sources"] = sources
    if domains:
        params["domains"] = domains
    if excludeDomains:
        params["excludeDomains"] = excludeDomains

    return get_response(url, headers={}, **params)


def get_news_headlines(api_key="", country=None, category=None, sources=None, q=None, pageSize=2, page=1):
    url = "https://newsapi.org/v2/top-headlines/"
    params = {
        "apiKey": api_key,
        "pageSize": pageSize,
        "page": page
    }

    if country:
        params["country"] = country
    if category:
        params["category"] = category
    if sources:
        params["sources"] = sources
    if q:
        params["q"] = q

    return get_response(url, headers={}, **params)


def get_news_headlines_sources(api_key="", country=None, category="business,entertainment,general,health,science,sports,technology", language="en"):
    url = " https://newsapi.org/v2/top-headlines/sources"
    params = {
        "apiKey": api_key,
        "category": category,
        "language": language
    }
    if country:
        params["country"] = country

    return get_response(url, headers={}, **params)


# 使用示例
if __name__ == "__main__":
    q = "technology"
    from_date = "2023-08-12"
    to_date = "2023-08-12"
    sort_by = "popularity"
    news_data = get_news_everything(
        q=q, from_date=from_date, to_date=to_date, sortBy=sort_by)
    print(news_data)

    # category = "science"
    # news_headlines = get_news_headlines(q=q, category=category)
    # print(news_headlines)

    # news_headlines_sources = get_news_headlines_sources()
    # print(news_headlines_sources)
