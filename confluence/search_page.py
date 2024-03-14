import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os, json
import requests

load_dotenv()

def search_page(title):

    api_endpoint_search = f'{os.getenv("ATLASSIAN_URL")}wiki/api/v2/pages?title={title}'
    print(api_endpoint_search)
    
    response = requests.get(api_endpoint_search, auth=HTTPBasicAuth(os.getenv("ATLASSIAN_USERNAME"),os.getenv("ATLASSIAN_PASSWORD")))

    # Check if the request was successful (status code 200) and if there are any results
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'results' in data and len(data['results']) > 0:
            id = data['results'][0]['id']
            version_number = data['results'][0]['version']['number']
            return [id, version_number]
        print("Page not found. Will create it")
        return [None, None]
    else:
        print("Error:", response.status_code)

#test = search_page("Version 2.33.0")
#print(test)