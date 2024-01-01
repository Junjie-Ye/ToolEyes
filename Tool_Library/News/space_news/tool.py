import requests


def get_response(url, headers, **kwargs):
    response = requests.get(url, headers=headers, params=kwargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_news_articles(
    event: list[int] = None,
    has_event: bool = None,
    has_launch: bool = None,
    launch: list[str] = None,
    limit: int = None,
    news_site: str = None,
    offset: int = None,
    ordering: str = None,
    published_at_gt: str = None,
    published_at_gte: str = None,
    published_at_lt: str = None,
    published_at_lte: str = None,
    search: str = None,
    summary_contains: str = None,
    summary_contains_all: str = None,
    summary_contains_one: str = None,
    title_contains: str = None,
    title_contains_all: str = None,
    title_contains_one: str = None,
    updated_at_gt: str = None,
    updated_at_gte: str = None,
    updated_at_lt: str = None,
    updated_at_lte: str = None,
):
    url = "https://api.spaceflightnewsapi.net/v4/articles/"
    params = {
    }

    if event:
        params["event"] = event
    if has_event:
        params["has_event"] = has_event
    if has_launch:
        params["has_launch"] = has_launch
    if launch:
        params["launch"] = launch
    if limit:
        params["limit"] = limit
    if news_site:
        params["news_site"] = news_site
    if offset:
        params["offset"] = offset
    if ordering:
        params["ordering"] = ordering
    if published_at_gt:
        params["published_at__gt"] = published_at_gt
    if published_at_gte:
        params["published_at__gte"] = published_at_gte
    if published_at_lt:
        params["published_at__lt"] = published_at_lt
    if published_at_lte:
        params["published_at__lte"] = published_at_lte
    if search:
        params["search"] = search
    if summary_contains:
        params["summary_contains"] = summary_contains
    if summary_contains_all:
        params["summary_contains_all"] = summary_contains_all
    if summary_contains_one:
        params["summary_contains_one"] = summary_contains_one
    if title_contains:
        params["title_contains"] = title_contains
    if title_contains_all:
        params["title_contains_all"] = title_contains_all
    if title_contains_one:
        params["title_contains_one"] = title_contains_one
    if updated_at_gt:
        params["updated_at__gt"] = updated_at_gt
    if updated_at_gte:
        params["updated_at__gte"] = updated_at_gte
    if updated_at_lt:
        params["updated_at__lt"] = updated_at_lt
    if updated_at_lte:
        params["updated_at__lte"] = updated_at_lte

    return get_response(url, headers={}, **params)


def get_news_articles_by_id(
    id: int
):
    url = 'https://api.spaceflightnewsapi.net/v4/articles/{}/'.format(id)
    params = {
    }
    return get_response(url, headers={}, **params)


def get_news_blogs(
    event: list[int] = None,
    has_event: bool = None,
    has_launch: bool = None,
    launch: list[str] = None,
    limit: int = None,
    news_site: str = None,
    offset: int = None,
    ordering: str = None,
    published_at_gt: str = None,
    published_at_gte: str = None,
    published_at_lt: str = None,
    published_at_lte: str = None,
    search: str = None,
    summary_contains: str = None,
    summary_contains_all: str = None,
    summary_contains_one: str = None,
    title_contains: str = None,
    title_contains_all: str = None,
    title_contains_one: str = None,
    updated_at_gt: str = None,
    updated_at_gte: str = None,
    updated_at_lt: str = None,
    updated_at_lte: str = None,
):
    url = "https://api.spaceflightnewsapi.net/v4/blogs/"
    params = {
    }

    if event:
        params["event"] = event
    if has_event:
        params["has_event"] = has_event
    if has_launch:
        params["has_launch"] = has_launch
    if launch:
        params["launch"] = launch
    if limit:
        params["limit"] = limit
    if news_site:
        params["news_site"] = news_site
    if offset:
        params["offset"] = offset
    if ordering:
        params["ordering"] = ordering
    if published_at_gt:
        params["published_at__gt"] = published_at_gt
    if published_at_gte:
        params["published_at__gte"] = published_at_gte
    if published_at_lt:
        params["published_at__lt"] = published_at_lt
    if published_at_lte:
        params["published_at__lte"] = published_at_lte
    if search:
        params["search"] = search
    if summary_contains:
        params["summary_contains"] = summary_contains
    if summary_contains_all:
        params["summary_contains_all"] = summary_contains_all
    if summary_contains_one:
        params["summary_contains_one"] = summary_contains_one
    if title_contains:
        params["title_contains"] = title_contains
    if title_contains_all:
        params["title_contains_all"] = title_contains_all
    if title_contains_one:
        params["title_contains_one"] = title_contains_one
    if updated_at_gt:
        params["updated_at__gt"] = updated_at_gt
    if updated_at_gte:
        params["updated_at__gte"] = updated_at_gte
    if updated_at_lt:
        params["updated_at__lt"] = updated_at_lt
    if updated_at_lte:
        params["updated_at__lte"] = updated_at_lte

    return get_response(url, headers={}, **params)


def get_news_blogs_by_id(
    id: int
):
    url = 'https://api.spaceflightnewsapi.net/v4/blogs/{}/'.format(id)
    params = {
    }
    return get_response(url, headers={}, **params)


def get_news_info():
    url = "https://api.spaceflightnewsapi.net/v4/info/"
    params = {
    }

    return get_response(url, headers={}, **params)


def get_news_reports(
    limit: int = None,
    news_site: str = None,
    offset: int = None,
    ordering: str = None,
    published_at_gt: str = None,
    published_at_gte: str = None,
    published_at_lt: str = None,
    published_at_lte: str = None,
    search: str = None,
    summary_contains: str = None,
    summary_contains_all: str = None,
    summary_contains_one: str = None,
    title_contains: str = None,
    title_contains_all: str = None,
    title_contains_one: str = None,
    updated_at_gt: str = None,
    updated_at_gte: str = None,
    updated_at_lt: str = None,
    updated_at_lte: str = None,
):
    url = "https://api.spaceflightnewsapi.net/v4/reports/"
    params = {
    }

    if limit:
        params["limit"] = limit
    if news_site:
        params["news_site"] = news_site
    if news_site:
        params["news_site"] = news_site
    if offset:
        params["offset"] = offset
    if ordering:
        params["ordering"] = ordering
    if published_at_gt:
        params["published_at__gt"] = published_at_gt
    if published_at_gte:
        params["published_at__gte"] = published_at_gte
    if published_at_lt:
        params["published_at__lt"] = published_at_lt
    if published_at_lte:
        params["published_at__lte"] = published_at_lte
    if search:
        params["search"] = search
    if summary_contains:
        params["summary_contains"] = summary_contains
    if summary_contains_all:
        params["summary_contains_all"] = summary_contains_all
    if summary_contains_one:
        params["summary_contains_one"] = summary_contains_one
    if title_contains:
        params["title_contains"] = title_contains
    if title_contains_all:
        params["title_contains_all"] = title_contains_all
    if title_contains_one:
        params["title_contains_one"] = title_contains_one
    if updated_at_gt:
        params["updated_at__gt"] = updated_at_gt
    if updated_at_gte:
        params["updated_at__gte"] = updated_at_gte
    if updated_at_lt:
        params["updated_at__lt"] = updated_at_lt
    if updated_at_lte:
        params["updated_at__lte"] = updated_at_lte

    return get_response(url, headers={}, **params)


def get_news_reports_by_id(
    id: int
):
    url = 'https://api.spaceflightnewsapi.net/v4/reports/{}/'.format(id)
    params = {
    }

    return get_response(url, headers={}, **params)


# 使用示例
if __name__ == "__main__":

    # result = get_news_articles(limit=1)
    # print(result)
    # result = get_news_articles_by_id(id=2)
    # print(result)
    # result = get_news_blogs(limit=2)
    # print(result)
    # result = get_news_blogs_by_id(id=2)
    # print(result)
    # result = get_news_info()
    # print(result)
    # result = get_news_reports(limit=3)
    # print(result)
    result = get_news_reports_by_id(id=3)
    print(result)
