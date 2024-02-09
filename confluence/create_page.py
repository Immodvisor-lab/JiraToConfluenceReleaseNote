from dotenv import load_dotenv
import os
import json
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def create_page(html, title):

    url = f'{os.getenv("ATLASSIAN_URL")}/wiki/api/v2/pages'

    payload = {
        "spaceId": os.getenv("CONFLUENCE_SPACE_ID"),
        "title": title,
        "parentId": os.getenv("CONFLUENCE_PARENT_ID"),
        "body": {
            "representation": "storage",
            "value": html,
        }
    }
    payload_json = json.dumps(payload)

    basic_auth = HTTPBasicAuth(os.getenv("ATLASSIAN_USERNAME"), os.getenv("ATLASSIAN_PASSWORD"))

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    confluence_answer = requests.post(url=url, data=payload_json, headers=headers, auth=basic_auth)
