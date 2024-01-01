from urllib import parse
import requests
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def parse_html_to_json(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    entries = []
    for entry in soup.find_all('queryresult'):
        entry_dict = {}
        try:
            meta_info = entry.find('pod')
            root = ET.fromstring(str(meta_info))
            attributes = dict(root.attrib)
        except:
            attributes = 'there is no info under pod token'

        try:
            recommend = entry.find('didyoumean').get_text()
        except:
            recommend = 'no recommend question'
        try:
            results = entry.find_all('plaintext')
            results_series = [res.get_text() for res in results]
            if not results_series:
                results_series = 'no results, try recommended questions'
        except:
            results_series = 'no results, try recommended questions'

        entry_dict['meta_info'] = attributes
        entry_dict['results'] = results_series
        entry_dict['recommend'] = recommend

        entries.append(entry_dict)

    return json.dumps(entries, indent=4)


def get_wolfram_results(query, appid=""):
    base_url = "http://api.wolframalpha.com/v2/query"
    input = parse.quote(query)
    url = base_url + "?appid=" + appid + "&input=" + input + "&includepodid=Result"
    results = requests.get(url).content
    json_results = parse_html_to_json(results)
    return json_results


if __name__ == '__main__':
    query = 'countries in South America'
    appid = ""
    print(get_wolfram_results(query, appid))
