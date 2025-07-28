import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

def search_issues_in_version(version, include_epics=True):

    if include_epics:
        issue_types = "(Story, Epic)"
    else:
        issue_types = "(Story)"
    
    jql = f'project = {os.getenv("JIRA_PROJECT")} AND issuetype in {issue_types} AND fixVersion = "{version}"'

    if os.getenv("EXTRA_JQL"):
       jql += os.getenv("EXTRA_JQL")

    api_endpoint_search = f'{os.getenv("ATLASSIAN_URL")}/rest/api/3/search'
    params = {
        'jql': jql,
        'fields': [
            os.getenv("JIRA_FIELD_KEY"),
            os.getenv("JIRA_FIELD_TITLE"),
            os.getenv("JIRA_FIELD_CONTENT"),
        ],
        'expand': [
            "renderedFields",
        ],
    }

    jira_answer = requests.post(
        api_endpoint_search, 
        auth=HTTPBasicAuth(os.getenv("ATLASSIAN_USERNAME"), os.getenv("ATLASSIAN_PASSWORD")),
        json=params
    )

    if jira_answer.status_code != 200:
        print("Call to Jira returned with code "+str(jira_answer.status_code))
        raise Exception("Failed to search for issues. Check if your version does not have remaining spaces. Error: "+str(jira_answer.content))

    issues = jira_answer.json()['issues']

    if len(issues) == 0:
        raise Exception("This version contains no "+os.getenv("JIRA_ISSUE_TYPE"))

    return issues