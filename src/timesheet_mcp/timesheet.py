import requests
import timesheet_mcp.models as models

class TimesheetClient:
    token = None
    def __init__(self, username: str = None, password: str = None, token: str = None, base_url: str = "https://timesheet.actum.cz/api"):
        self.base_url = base_url
        if token:
            self.token = token
        elif username and password:
            self.token = self.login(username, password)
        else:
            raise ValueError("Either username/password or token must be provided.")

    def login(username: str, password: str, base_url: str = "https://timesheet.actum.cz/api") -> str:
        url = f"{base_url}/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.text.strip('"')
        else:
            raise Exception("Login failed: " + response.text)

    def get_projects(self) -> list[models.Project]:
        url = f"{self.base_url}/projects"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [models.Project(**project) for project in response.json()]
        else:
            raise Exception("Failed to fetch projects: " + response.text)
        
    def get_activities(self, project_id: int) -> list[models.Activity]:
        url = f"{self.base_url}/projects/{project_id}/activities"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [models.Activity(**activity) for activity in response.json()]
        else:
            raise Exception("Failed to fetch activities: " + response.text)
        
    def get_issues(self, project_id: int) -> list[models.Issue]:
        url = f"{self.base_url}/projects/{project_id}/issues"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [models.Issue(**issue) for issue in response.json()]
        else:
            raise Exception("Failed to fetch issues: " + response.text)

    def get_timesheets(self, start_date: str, end_date: str) -> list[models.TimesheetEntry]:
        url = f"{self.base_url}/timeEntries?from={start_date}&to={end_date}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [models.TimesheetEntry(**entry) for entry in response.json()]
        else:
            raise Exception("Failed to fetch timesheets: " + response.text)
        
    def add_timesheet_entry(self, entry: models.TimesheetEntryInput) -> list[models.TimesheetEntry]:
        url = f"{self.base_url}/timeEntries"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = entry.to_create_dict()
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return [models.TimesheetEntry(**entry["time_entry"]) for entry in response.json()]
        else:
            print("Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("Failed to add timesheet entry: " + response.text)
        
    def edit_timesheet_entry(self, entry_id: int ,entry: models.TimesheetEntryInput) -> str:
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