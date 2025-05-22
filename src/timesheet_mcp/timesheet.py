import requests
from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
import re


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

    @field_validator("spent_on", mode="before")
    @classmethod
    def adjust_spent_on(cls, value: str) -> str:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return value
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)
        if (dt - midnight) <= (next_midnight - dt):
            adjusted = midnight
        else:
            adjusted = next_midnight
        return adjusted.date().isoformat()

class TimesheetEntryInput(BaseModel):
    hours: float
    comments: str
    activity_id: int
    project_id: int
    date: str
    issue_id: int | None = None

    def to_create_dict(self) -> dict[str, dict[str, str | dict[str, str | int| None]]]:
            return {
            "interval": {
                "start": self.date,
                "end": self.date
            },
            "timeEntry": {
                "time_entry": {
                    "activity_id": self.activity_id,
                    "issue_id": self.issue_id,
                    "comments": self.comments,
                    "hours": str(self.hours),
                    "project_id": self.project_id,
                    "spent_on": self.date
                }
            }
        }

    def to_update_dict(self) -> dict[str, dict[str, str | dict[str, str | int| None]]]:
        return {
            "timeEntryUpdate": {
                    "time_entry": {
                        "activity_id": self.activity_id,
                        "issue_id": self.issue_id,
                        "comments": self.comments,
                        "hours": str(self.hours),
                        "project_id": self.project_id,
                        "spent_on": self.date
                    }
                }
        }

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
            return [Project(**project) for project in response.json()]
        else:
            raise Exception("Failed to fetch projects: " + response.text)
        
    def get_activities(self, project_id: int) -> list[Activity]:
        url = f"{self.base_url}/projects/{project_id}/activities"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [Activity(**activity) for activity in response.json()]
        else:
            raise Exception("Failed to fetch activities: " + response.text)
        
    def get_issues(self, project_id: int) -> list[Issue]:
        url = f"{self.base_url}/projects/{project_id}/issues"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [Issue(**issue) for issue in response.json()]
        else:
            raise Exception("Failed to fetch issues: " + response.text)

    def get_timesheets(self, start_date: str, end_date: str) -> list[TimesheetEntry]:
        url = f"{self.base_url}/timeEntries?from={start_date}&to={end_date}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [TimesheetEntry(**entry) for entry in response.json()]
        else:
            raise Exception("Failed to fetch timesheets: " + response.text)
        
    def add_timesheet_entry(self, entry: TimesheetEntryInput) -> TimesheetEntry:
        url = f"{self.base_url}/timeEntries"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = entry.to_create_dict()
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return TimesheetEntry(**response.json())
        else:
            print("Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("Failed to add timesheet entry: " + response.text)
        
    def edit_timesheet_entry(self, entry_id: int ,entry: TimesheetEntryInput) -> str:
        url = f"{self.base_url}/timeEntries/{entry_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = entry.to_update_dict()
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.text.strip('"')
        else:
            print("Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("Failed to edit timesheet entry: " + response.text)
    
    def delete_timesheet_entry(self, entry_id: int) -> bool:
        url = f"{self.base_url}/timeEntries/{entry_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print("Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("Failed to delete timesheet entry: " + response.text)