import requests
from bs4 import BeautifulSoup
import json

def get_response(url, **kwargs):
    headers={"Content-Type" : "json"}
    response = requests.get(url, headers=headers, params=kwargs)
    return response.text

def parse_html_to_json(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    
    entries = []
    for entry in soup.find_all('entry'):
        entry_dict = {}
        title = entry.find('title').get_text()
        summary = entry.find('summary').get_text()
        link = entry.find('link')['href']
        
        entry_dict['title'] = title
        entry_dict['summary'] = summary
        entry_dict['link'] = link
        
        entries.append(entry_dict)
    
    return json.dumps(entries, indent=4)

def arxiv_query(search_query: str = None, id_list: str = None, start: int = 0, max_results: int = 10):
    url = "http://export.arxiv.org/api/query"
    params = {
        "start": start,
        "max_results": max_results
    }

    if search_query:
        params["search_query"] = search_query
    if id_list:
        params["id_list"] = id_list

    html_response = get_response(url, **params)
    json_response = parse_html_to_json(html_response)
    
    return json_response

# 使用示例
if __name__ == "__main__":
    json_response = arxiv_query(search_query="language model", start=1, max_results=3)
    print(json_response)
