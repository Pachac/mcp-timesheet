import requests
from pydantic import BaseModel
import json

class Project(BaseModel):
    id: int
    name: str
    parent: str | None = None
    grandparent: str | None = None

class Activity(BaseModel):
    id: int
    name: str

class Issue(BaseModel):
    id: int | None = None
    subject: str | None = None

class TimesheetEntry(BaseModel):
    id: int
    hours: float
    comments: str
    activity: Activity
    project: Project
    issue: Issue
    spent_on: str


class TimesheetClient:
    token = None
    def __init__(self, username: str, password: str):
        self.base_url = "https://timesheet.actum.cz/api"
        self.login(username, password)

    def login(self, username: str, password: str):
        url = f"{self.base_url}/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.text.strip('"')
        else:
            raise Exception("Login failed: " + response.text)

    def get_projects(self) -> list[Project]:
        url = f"{self.base_url}/projects"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch projects: " + response.text)
        
    def get_activities(self, project_id: int) -> list[Activity]:
        url = f"{self.base_url}/projects/{project_id}/activities"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch activities: " + response.text)
        
    def get_issues(self, project_id: int) -> list[Issue]:
        url = f"{self.base_url}/projects/{project_id}/issues"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch issues: " + response.text)

    def get_timesheets(self, start_date: str, end_date: str) -> list[TimesheetEntry]:
        url = f"{self.base_url}/timeEntries?from={start_date}&to={end_date}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch timesheets: " + response.text)
        
    def add_timesheet(self, 
                      project_id: int,
                      activity_id: int,
                      date: str, 
                      hours: float, 
                      description: str,
                      issue_id: int = None) -> TimesheetEntry:
        url = f"{self.base_url}/timeEntries"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "interval": {
                "start": date,
                "end": date
            },
            "timeEntry": {
                "time_entry": {
                    "activity_id": activity_id,
                    "issue_id": issue_id,
                    "comments": description,
                    "hours": str(hours),
                    "project_id": project_id,
                    "spent_on": date
                }
            }
        }
        print(json.dumps(data, indent=4))
        if issue_id:
            data["timeEntry"]["issue_id"] = issue_id
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            print("Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("Failed to add timesheet entry: " + response.text)