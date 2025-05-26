from pydantic import BaseModel, field_validator
import re
from datetime import datetime, timedelta

def sanitize_string(value):
    """
    Sanitize a string by removing leading and trailing whitespace.
    """
    if not isinstance(value, str):
        return value
    return value.replace("|", "\\|").strip()

class BaseTimesheetClass(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def validate_non_empty(cls, value):
        return sanitize_string(value)


class RedmineUser(BaseTimesheetClass):
    id: int
    name: str

class Project(BaseTimesheetClass):
    id: int
    name: str
    parent: str | None = None
    grandparent: str | None = None

class Activity(BaseTimesheetClass):
    id: int
    name: str

class Issue(BaseTimesheetClass):
    id: int | None = None
    subject: str | None = None

class TimesheetEntry(BaseTimesheetClass):
    id: int
    hours: float
    comments: str
    activity: Activity
    project: Project
    issue: Issue | None = None
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

class TimesheetEntryInput(BaseTimesheetClass):
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
