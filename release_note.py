from jira.search_issues import search_issues_in_version
from jira.get_versions import get_versions
from issue import Issue
from datetime import datetime
from dotenv import load_dotenv
import os
from confluence.create_page import create_page

load_dotenv()

class ReleaseNote:
    def __init__(self):
        self.issues = []
        self.final_content = []

    def __content(self):
        return self.content

    def __title(self):
        return "Version "+self.version
    
    def url(self):
        return os.getenv("ATLASSIAN_URL")
    
    def set_version(self):
        
        versions = get_versions()

        print("Choose a version :")
        for index, version in enumerate(versions, start=1):
            print(f"{index}. Name: {version['name']}, Release Date: {version['releaseDate']}")
        
        # Get user input for the chosen version
        while True:
            try:
                choice = int(input("Enter the number of the version you want to choose: "))
                if 1 <= choice <= len(versions):
                    selected_version = versions[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        self.version = selected_version['name']

        release_date_object = datetime.strptime(selected_version['releaseDate'], '%Y-%m-%d')
        self.release_date = release_date_object.strftime('%d/%m/%y')

    def set_issues(self):
        try:
            jira_issues = search_issues_in_version(self.version)
            for issue_jira in jira_issues:
                self.issues.append(Issue(issue_jira))
        except Exception as e:
            print(e)
            exit()

    def set_content(self):
        self.content = "<p>Date de mise en ligne : "+self.release_date+"</p>"
        for issue in self.issues:
            if isinstance(issue, Issue):
                self.content += "\n"+issue.get_final_content()
        return self.content

    def __search_page(self):
        try:
            return False
            #page_already_exists_id = search_page(self.version)
            #return page_already_exists_id
        except IndexError:
            return False

    def create_or_update(self):
        #id_page = self.__search_page()
        #try: 
        #if(id_page == False):
        create_page(
            self.__content(),
            self.__title(),
        )
        print("Release note for version "+self.version+" successfully created.")
"""             else:
            update_page(
                id_page,
                self.__content(),
                self.__description(),
                self.__tags(),
                self.__title(),
            )
            print("Release note for version "+self.version+" successfully updated.") """
        #except Exception as e:
        #    print("Page creation / update for release note on version "+self.version+" FAILED.")
        #    print(e.args) 
        
