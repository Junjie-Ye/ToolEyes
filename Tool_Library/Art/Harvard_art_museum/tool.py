import requests

#api_key=""
#base_url="https://api.harvardartmuseums.org/"

def get_response(url, **kargs):
    response = requests.get(url, params=kargs)
    try:
        observation = response.json()
    except:
        observation = response.textF
    return observation

def search_resource(res_type:str,q:str="",size:int=10,page:int=1,sort:str="random",sortorder:str="asc",apikey:str="",fields:str="",id:str="",agg:str="",**add_params):
    res_type=res_type.lower()
    url=f"https://api.harvardartmuseums.org/{res_type}?apikey={apikey}&size={size}&page={page}&sort={sort}&sortorder={sortorder}"
    if(len(fields)>0):
        url+=f"&fields={fields}"
    if(len(id)>0):
        url+=f"id={id}"
    if(len(agg)!=0):
        url+=f"&aggregation={agg}"
    if(len(q)>0):
        url+=f"&q={q}"
    for key, value in add_params.items():
        url += f"&{key}={value}"

    return get_response(url)

def get_resource_by_id(res_type:str,id:int,apikey:str=""):
    url=f"https://api.harvardartmuseums.org/{res_type}/{id}?apikey={apikey}" 
    return get_response(url)   

def get_resource_in_iiif(res_type:str,id:int):
    url=f"https://iiif.harvardartmuseums.org/manifests/{res_type}/{id}"
    return get_response(url)

if __name__ == '__main__':
    #print(search_resource("color",size=3,fields='name'))
    print(search_resource("object",person=33430))
    #print(search_info("activity",size=3,object=6772,type='pageviews'))
    #print (get_resource_by_id("gallery",1600))
    #print(get_resource_in_iiif("gallery",1600))