from dotenv import load_dotenv
import os
import json
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def create_or_update_page(html, title, id_page=None, version_number=None):

    update = True if id_page else False

    url = f'{os.getenv("ATLASSIAN_URL")}/wiki/api/v2/pages{"/"+id_page if update else ""}'

    payload = {
        "title": title,
        "body": {
            "representation": "storage",
            "value": html,
        },
        **({"parentId": os.getenv("CONFLUENCE_PARENT_ID")} if not update else {}),
        **({"spaceId": os.getenv("CONFLUENCE_SPACE_ID")} if not update else {}),
        **({"status": "current"} if update else {}),
        **({"id": id_page} if update else {}),
        **({"version": {"number": version_number+1, "message": "Automatic update"}} if update else {}),
    }
    payload_json = json.dumps(payload)

    basic_auth = HTTPBasicAuth(os.getenv("ATLASSIAN_USERNAME"), os.getenv("ATLASSIAN_PASSWORD"))

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    if(not update):
        confluence_answer = requests.post(url=url, data=payload_json, headers=headers, auth=basic_auth)
    else: 
        confluence_answer = requests.put(url=url, data=payload_json, headers=headers, auth=basic_auth)

    if confluence_answer.status_code != 200:
        print("Call to Jira returned with code "+str(confluence_answer.status_code))
        raise Exception("Failed to create page. Error: "+str(confluence_answer.content))
    else:
        print(confluence_answer)