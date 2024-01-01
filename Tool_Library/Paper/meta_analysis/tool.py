import requests

def get_response(url, headers, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation


def get_paper_complete(query:str):
    url = "https://api.semanticscholar.org/graph/v1/paper/autocomplete"
    params = {
        "query": query
    }

    return get_response(url, headers={}, **params)


def get_papers_by_keywords(
        query:str,
        fields:str = None,
        publicationTypes:str = None,
        openAccessPdf:str = None,
        year:str = None,
        venue:str = None,
        fieldsOfStudy:str = None,
        offset:int = 0,
        limit:int = 100
    ):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "offset": offset,
        "limit": limit
    }

    if fields:
        params["fields"] = fields
    if publicationTypes:
        params["publicationTypes"] = publicationTypes
    if openAccessPdf:
        params["openAccessPdf"] = openAccessPdf
    if year:
        params["year"] = year
    if venue:
        params["venue"] = venue
    if fieldsOfStudy:
        params["fieldsOfStudy"] = fieldsOfStudy

    return get_response(url, headers={}, **params)


def get_paper_details(paper_id:str, fields:str = None):
    url = 'https://api.semanticscholar.org/graph/v1/paper/{}'.format(paper_id)
    params = {}
    if fields:
        params["fields"] = fields
    
    return get_response(url, headers={}, **params)


def get_author_by_name(query:str, offset:int = 0, limit:int = 100, fields:str = None):
    url = 'https://api.semanticscholar.org/graph/v1/author/search'

    params = {
        "query": query,
        "offset": offset,
        "limit": limit
    }
    if fields:
        params["fields"] = fields
    
    return get_response(url, headers={}, **params)


def get_author_details(author_id:str, fields:str = None):
    url = 'https://api.semanticscholar.org/graph/v1/author/{}'.format(author_id)
    params = {}
    if fields:
        params["fields"] = fields
    
    return get_response(url, headers={}, **params)

def get_author_papers(author_id:str,  offset:int = 0, limit:int = 100, fields:str = None):
    url = 'https://api.semanticscholar.org/graph/v1/author/{}/papers'.format(author_id)
    params = {
        "offset": offset,
        "limit": limit
    }
    if fields:
        params["fields"] = fields
    
    return get_response(url, headers={}, **params)


# 使用示例
if __name__ == "__main__":
    query = "machine learning"  # Specify the query for testing

    # Test get_paper_complete function
    paper_complete_result = get_paper_complete(query=query)
    print("get_paper_complete result:", paper_complete_result)

    # Test get_papers_by_keywords function
    papers_by_keywords_result = get_papers_by_keywords(query=query, limit=5)
    print("get_papers_by_keywords result:", papers_by_keywords_result)

    # Assuming you have a valid paper_id for testing
    paper_id = "your_paper_id_here"

    # Test get_paper_details function
    paper_details_result = get_paper_details(paper_id=paper_id)
    print("get_paper_details result:", paper_details_result)

    # Test get_author_by_name function
    author_query = "John Doe"  # Specify the author query for testing
    author_by_name_result = get_author_by_name(query=author_query, limit=3)
    print("get_author_by_name result:", author_by_name_result)

    # Assuming you have a valid author_id for testing
    author_id = "your_author_id_here"

    # Test get_author_details function
    author_details_result = get_author_details(author_id=author_id)
    print("get_author_details result:", author_details_result)

    # Test get_author_papers function
    author_papers_result = get_author_papers(author_id=author_id, limit=5)
    print("get_author_papers result:", author_papers_result)
