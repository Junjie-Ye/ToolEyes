import requests


def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def blog_entry_comments(blog_entry_id: int):
    url = f' https://codeforces.com/api/blogEntry.comments?blogEntryId={blog_entry_id}'

    return get_response(url)


def blog_entry_view(blog_entry_id: int):
    url = f' https://codeforces.com/api/blogEntry.view?blogEntryId={blog_entry_id}'

    return get_response(url)


def contest_hacks(contest_id: int, as_manager: bool = False):
    url = f' https://codeforces.com/api/contest.hacks?contestId={contest_id}&asManager={as_manager}'

    return get_response(url)


def contest_list(gym: bool = False):
    url = f' https://codeforces.com/api/contest.list?gym={gym}'

    return get_response(url)


def contest_rating_changes(contest_id: int):
    url = f' https://codeforces.com/api/contest.ratingChanges?contestId={contest_id}'

    return get_response(url)


def contest_standings(contest_id: int, as_manager: bool = False, from_id: int = 1, count: int = 5, handles: str = None, room: int = None, show_unofficial: bool = False):
    url = f' https://codeforces.com/api/contest.standings'
    params = {'contestId': contest_id, 'asManager': as_manager, 'from': from_id,
              'count': count, 'handles': handles, 'room': room, 'showUnofficial': show_unofficial}
    return get_response(url, **params)


def contest_status(contest_id: int, count: int, as_manager: bool = False, from_id: int = 1, handles: str = None):
    url = 'https://codeforces.com/api/contest.status'
    params = {'contestId': contest_id, 'asManager': as_manager,
              'from': from_id, 'count': count, 'handles': handles}
    return get_response(url, **params)


def problem_set_problems(tags: str = None, problem_set_name: str = None):
    url = f' https://codeforces.com/api/problemset.problems'
    params = {'tags': tags, 'problemsetName': problem_set_name}
    return get_response(url, **params)


def problem_set_recent_status(count: int, problem_set_name: str = None):
    url = f' https://codeforces.com/api/problemset.recentStatus'
    params = {'count': count, 'problemsetName': problem_set_name}

    return get_response(url, **params)


def recent_actions(max_count: int):
    url = f' https://codeforces.com/api/recentActions?maxCount={max_count}'

    return get_response(url)


def user_blog_entries(handle: str):
    url = f' https://codeforces.com/api/user.blogEntries?handle={handle}'

    return get_response(url)


def user_friends(only_online: bool = False):
    url = f' https://codeforces.com/api/user.friends?onlyOnline={only_online}'

    return get_response(url)


def user_info(handle: str):
    url = f' https://codeforces.com/api/user.info?handles={handle}'

    return get_response(url)


def user_rated_list(active_only: bool = False, include_retired: bool = False, contest_id: int = None):
    url = f' https://codeforces.com/api/user.ratedList'
    params = {'activeOnly': active_only,
              'includeRetired': include_retired, 'contestId': contest_id}

    return get_response(url, **params)


def user_rating(handle: str):
    url = f' https://codeforces.com/api/user.rating?handle={handle}'

    return get_response(url)


def user_status(handle: str, count: int = 10, from_id: int = 1):
    url = f' https://codeforces.com/api/user.status'
    params = {'handle': handle, 'from': from_id, 'count': count}

    return get_response(url, **params)


if __name__ == '__main__':
    print(contest_standings(1))
