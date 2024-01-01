import requests

def get_response(url, **kargs):
    response = requests.get(url, kargs)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation

def list_of_kontests(contest_name:str):
    contest_name = contest_name.lower()
    url = f' https://kontests.net/api/v1/{contest_name}'

    return get_response(url)

# contest_name: all, codeforces, codeforces_gym, top_coder, 
# at_coder, code_chef, cs_academy, hacker_earth, hacker_rank, leet_code

if __name__ == '__main__':
    # print(list_of_kontests("all"))
    print(list_of_kontests("codeforces"))
    