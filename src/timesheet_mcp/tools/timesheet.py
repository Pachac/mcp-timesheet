from mcp import Tool
import timesheet as ts
import config as cfg

client = ts.TimesheetClient(
    username="tomas.pachovsky",
    password=cfg.TS_PW
)

def get_projects() -> list[ts.Project]:
    """
    Get all projects available to be filled in the timesheet
    :return: List of projects
    """
    projects = client.get_projects()
    return projects

def get_activities(project_id: int) -> list[ts.Activity]:
    """
    Get all activities available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of activities
    """
    activities = client.get_activities(project_id)
    return activities


def get_issues(project_id: int) -> list[ts.Issue]:
    """
    Get all issues available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of issues
    """
    issues = client.get_issues(project_id)
    return issues

def get_timesheets(start_date: str, end_date: str) -> list[ts.TimesheetEntry]:
    """
    Get all timesheet entries for a specific date range. The date format is YYYY-MM-DD.
    :param start_date: Start date of the timesheet
    :param end_date: End date of the timesheet
    :return: List of timesheet entries
    """
    timesheets = client.get_timesheets(start_date, end_date)
    return timesheets


def add_timesheet(
        project_id: int,
        activity_id: int,
        date: str, 
        hours: float, 
        description: str,
        issue_id: int = None) -> ts.TimesheetEntry:
    """
    Add a timesheet entry for a specific project, activity, and date. The date format is YYYY-MM-DD.
    :param project_id: ID of the project
    :param activity_id: ID of the activity
    :param date: Date of the timesheet entry
    :param hours: Number of hours worked
    :param description: Description of the timesheet entry
    :param issue_id: ID of the issue (optional)
    :return: Timesheet entry
    """
    timesheet = client.add_timesheet(project_id, activity_id, date, hours, description, issue_id)
    return timesheet
