import requests


def get_response(url):
    response = requests.get(url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


BASE_URL = "https://a.4cdn.org"


def get_limited_list(array, length, limit, offset):
    length = int(length)
    limit = int(limit)
    offset = int(offset)
    if offset < 0:
        offset = 0
    if offset >= length or limit <= 0:
        return []
    if offset + limit > length:
        limit = length - offset
    return array[offset: offset + limit]


def get_boards(page: int = 0, page_size: int = 5):
    page = int(page)
    page_size = int(page_size)
    boards = get_response(BASE_URL + "/boards.json")["boards"]
    return get_limited_list(boards, len(boards), page_size, page * page_size)


def get_threads(board: str, page: int = 1):
    page = int(page)
    response = get_response(BASE_URL + f"/{board}/threads.json")
    if page > len(response):
        return []
    return response[page - 1]["threads"]


def get_catalog(board: str, page: int = 1, limit: int = 3, offset: int = 0):
    page = int(page)
    limit = int(limit)
    offset = int(offset)
    response = get_response(BASE_URL + f"/{board}/catalog.json")
    if page > len(response):
        return []
    threads = response[page - 1]["threads"]
    return get_limited_list(threads, len(threads), limit, offset)


def get_archive(board: str):
    return get_response(BASE_URL + f"/{board}/archive.json")


def get_threads_with_preview(board: str, page: int = 1, limit: int = 3, offset: int = 0):
    page = int(page)
    limit = int(limit)
    offset = int(offset)
    response = get_response(BASE_URL + f"/{board}/{page}.json")
    try:
        threads = response["threads"]
        return get_limited_list(threads, len(threads), limit, offset)
    except:
        return []


def get_posts(board: str, thread_no: int):
    return get_response(BASE_URL + f"/{board}/thread/{thread_no}.json")


if __name__ == "__main__":
    # print(get_boards())
    print(get_threads("po", "1"))
    # print(get_catalog("po"))
    # print(get_archive("po"))
    # print(get_threads_with_preview("po", 3))
