from dotenv import load_dotenv
import os

load_dotenv()

class Issue:
    def __init__(self, jira_issue):

        self.key = jira_issue[os.getenv("JIRA_FIELD_KEY")]
        print('-- processing issue '+self.key+'...')
        #print(json.dumps(jira_issue, indent=4))
        self.title = jira_issue['fields'][os.getenv("JIRA_FIELD_TITLE")]
        self.content = jira_issue['renderedFields'][os.getenv("JIRA_FIELD_CONTENT")]
        self.link = os.getenv("ATLASSIAN_URL") + "/browse/" + self.key

    def get_final_content(self):
        return f'<h1><a href="{self.link}">{self.key} - {self.title}</a></h1> \n {self.content} \n'