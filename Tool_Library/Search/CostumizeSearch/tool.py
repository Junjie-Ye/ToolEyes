import requests
import serpapi
# There is no avaliable pachage for serpapi at pypi, please download and install it at https://github.com/serpapi/serpapi-python.git
import warnings
from bs4 import BeautifulSoup


def get_default_serpapi_key():
    api_key = ""
    return api_key


def clean_str(p):
    return p.encode().decode("unicode-escape").encode("latin1").decode("utf-8")


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


class WikiPage:
    def __init__(self):
        self.page = ""
        self.paragraphs = []
        self.sentences = []
        self.lookup_cnt = 0
        self.lookup_list = []
        self.lookup_keyword = None

    def reset_page(self):
        self.page = ""
        self.paragraphs = []
        self.sentences = []
        self.lookup_cnt = 0
        self.lookup_list = []
        self.lookup_keyword = None

    def get_page_obs(self, page):
        self.page = page
        paragraphs = []
        sentences = []
        # find all paragraphs
        paragraphs = page.split("\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # find all sentence
        sentences = []
        for p in paragraphs:
            sentences += p.split('. ')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        self.paragraphs = paragraphs
        self.sentences = sentences
        return ' '.join(sentences[:5])

    def construct_lookup_list(self, keyword: str):
        sentences = self.sentences
        parts = []
        for index, p in enumerate(sentences):
            if keyword.lower() in p.lower():
                parts.append(index)
        self.lookup_list = parts
        self.lookup_keyword = keyword
        self.lookup_cnt = 0


def get_nobel_results(year=2022, nobelPrizeCategory="phy", csvLang="en"):
    year = str(year)
    request_url = "https://api.nobelprize.org/2.1/nobelPrizes?nobelPrizeYear=" + year \
        + "&nobelPrizeCategory=" + nobelPrizeCategory \
        + "&format=json&csvLang=" + csvLang
    results = requests.get(request_url)
    if not results.status_code == 200:
        warnings.warn("NobelPrizes Api Request Failed")
    return results.content


def google_events_search(query, api_key=None, **kwargs):
    engine = 'google_events'
    query = "events in " + query
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    try:
        return results['events_results']
    except KeyError:
        return "Wrong Query with no Events, Please Input a Location Like US"


def wiki_search(entity: str):
    currentPage = WikiPage()
    entity_ = entity.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    response_text = requests.get(search_url).text
    soup = BeautifulSoup(response_text, features="html.parser")
    result_divs = soup.find_all("div", {"class": "mw-search-result-heading"})
    if result_divs:  # mismatch
        result_titles = [clean_str(div.get_text().strip())
                         for div in result_divs]
        obs = f"Could not find {entity}. Similar: {result_titles[:5]}."
    else:
        local_page = [p.get_text().strip()
                      for p in soup.find_all("p") + soup.find_all("ul")]
        if any("may refer to:" in p for p in local_page):
            obs = wiki_search("[" + entity + "]")
        else:
            currentPage.reset_page()
            page = ""
            for p in local_page:
                if len(p.split(" ")) > 2:
                    page += clean_str(p)
                if not p.endswith("\n"):
                    page += "\n"
            obs = currentPage.get_page_obs(page)
    return obs


def google_autocomplete_search(query, api_key=None, **kwargs):
    engine = 'google_autocomplete'
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['suggestions']


def google_related_question_search(query, api_key=None, **kwargs):
    engine = 'google'
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['related_searches']


def google_patents_search(query, api_key=None, **kwargs):
    engine = 'google_patents'
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


def google_local_services_search(query, api_key=None, **kwargs):
    engine = 'google_local_services'
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['local_place']


def google_scholar_search(query, api_key=None, **kwargs):
    engine = 'google_scholar'
    if not api_key:
        api_key = get_default_serpapi_key()
    results = get_search_results(engine, q=query, api_key=api_key, **kwargs)
    return results['organic_results']


if __name__ == '__main__':
    # print(str(get_nobel_results()))
    print(google_scholar_search('gpt2', as_ylo=2022, hi='en', num=5))
    pass
