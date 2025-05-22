import requests
import requests.auth
import timesheet_mcp.models as models

class RedmineClient:
    def __init__(self, username: str, password: str):
        self.base_url = "https://support.actum.cz"
        self.auth = requests.auth.HTTPBasicAuth(username, password)

    def get_project_timesheet(
            self,
            start_date: str, 
            end_date: str,
            project_id: int | None = None,
            ) -> list[models.TimesheetEntry]:
        url = f"{self.base_url}/projects/{project_id}/time_entries.json?from={start_date}&to={end_date}"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return [response.json()["time_entries"]]
        else:
            raise Exception("Failed to fetch timesheet: " + response.text)
        
        