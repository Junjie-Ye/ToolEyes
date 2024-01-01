import requests


# def get_response(url, headers:dict = {}, kargs:dict = {}):
# if len(headers) > 0 and len(kargs) > 0:
#     response = requests.get(url, headers = headers, params=kargs)
# elif len(headers) > 0:
#     response = requests.get(url, headers=headers)
# elif len(kargs) > 0:
#     response = requests.get(url, params=kargs)
# else:
#     response = requests.get(url)
# try:
#     observation = response.json()
#     response.close()
# except:
#     observation = response.text
#     response.close()
# response.close()
# return observation
def get_response(url, headers=None, **kargs):
    response = requests.get(url, headers=headers, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.text

    return observation


def company_name_match(function: str = 'match', apikey: str = '', source: str = 'CSV', connection: str = 'https://dl.interzoid.com/csv/companies.csv', table: str = 'CSV', column: str = '1', process: str = 'matchreport', category: str = 'company', json: str = None, html: str = None):
    # url = f'https://connect.interzoid.com/run?function={function}&apikey={apikey}&source={source}&connection={connection}&table={table}&column={column}&process={process}&category={category}'
    # url='https://connect.interzoid.com/run?function=match&apikey=&source=CSV&connection=https://dl.interzoid.com/csv/companies.csv&table=CSV&column=1&process=matchreport&category=company&html=true'
    # if len(json):
    #     url += f'json={json}'
    # if len(html):
    #     url += f'&html={html}'
    url = f'https://connect.interzoid.com/run'
    return get_response(url, function=function, apikey=apikey, source=source, connection=connection, table=table, column=column, process=process, category=category, json=json, html=html)


def gutendex(author_year_start: str = "", author_year_end: str = "", copyright: bool | None = None, ids: str = "", languages: str = "", mime_type: str = "", search: str = "", sort: str = "", topic: str = "", id: str = ""):
    # flag = 0
    url = 'https://gutendex.com/books'
    if id:
        url += f'/{id}'
        return get_response(url)
    # if len(author_year_start) > 0:
    #     if flag == 0:
    #         url += f'?author_year_start={author_year_start}'
    #         flag = 1
    #     else:
    #         url += f'&author_year_start={author_year_start}'
    # if len(author_year_end) > 0:
    #     if flag == 0:
    #         url += f'?author_year_end={author_year_end}'
    #         flag = 1
    #     else:
    #         url += f'&author_year_end={author_year_end}'
    # if len(copyright) > 0:
    #     if flag == 0:
    #         url += f'?copyright={copyright}'
    #         flag = 1
    #     else:
    #         url += f'&copyright={copyright}'
    # if len(ids) > 0:
    #     if flag == 0:
    #         url += f'?ids={ids}'
    #         flag = 1
    #     else:
    #         url += f'&ids={ids}'
    # if len(languages) > 0:
    #     if flag == 0:
    #         url += f'?languages={languages}'
    #         flag = 1
    #     else:
    #         url += f'&languages={languages}'
    # if len(mime_type) > 0:
    #     if flag == 0:
    #         url += f'?mime_type={mime_type}'
    #         flag = 1
    #     else:
    #         url += f'&mime_type={mime_type}'
    # if len(search) > 0:
    #     if flag == 0:
    #         url += f'?search={search}'
    #         flag = 1
    #     else:
    #         url += f'&search={search}'
    # if len(sort) > 0:
    #     if flag == 0:
    #         url += f'?sort={sort}'
    #         flag = 1
    #     else:
    #         url += f'&sort={sort}'
    # if len(topic) > 0:
    #     if flag == 0:
    #         url += f'?topic={topic}'
    #         flag = 1
    #     else:
    #         url += f'&topic={topic}'
    # if len(id) > 0:
    #     url += f'/{id}'
    return get_response(url, author_year_start=author_year_start, author_year_end=author_year_end, copyright=copyright, ids=ids, languages=languages, mime_type=mime_type, search=search, sort=sort, topic=topic, id=id)


def poetry(input_field: str = 'author', search_term: str = 'Shakespeare', search_type: str = '', output_field: str = '', form: str = ''):
    url = f'https://poetrydb.org/{input_field}/{search_term}'
    if len(search_type) > 0:
        url += f':{search_type}'
    if len(output_field) > 0:
        url += f'/{output_field}'
    if len(form):
        url += f'.{form}'
    return get_response(url)


def rent_estimate(address: str = None, latitude: float = None, longitude: float = None, propertyType: str = 'Single Family', bedrooms: int = 4, bathrooms: int = 2, squareFootage: int = 1600, maxRadius: float = 50, daysOld: int = None, compCount: int = 10, apikey: str = 'f5b0e007d0msh2b8e8dfc2cb1178p14eb53jsnf303a3bd5f27'):
    url = 'https://realtymole-rental-estimate-v1.p.rapidapi.com/rentalPrice'
    headers = {
        "X-RapidAPI-Key": f'{apikey}',
        "X-RapidAPI-Host": "realtymole-rental-estimate-v1.p.rapidapi.com"
    }

    return get_response(url, headers, address=address, latitude=latitude, longitude=longitude, propertyType=propertyType, bedrooms=bedrooms, bathrooms=bathrooms, squareFootage=squareFootage, maxRadius=maxRadius)


if __name__ == '__main__':
    # print(company_name_match())
    # print(gutendex(author_year_start='1900', languages='en'))
    # print(poetry())
    print(rent_estimate(latitude=23.1, longitude=27.8))
