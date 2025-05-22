from mcp.server.fastmcp import FastMCP
import timesheet as ts
import config as cfg
import os

app = FastMCP(
    name="Timesheet",
    instructions="Timesheet Management System"
)

ts_client = ts.TimesheetClient(
    username="tomas.pachovsky",
    password=cfg.TS_PW
)

@app.tool()
def get_projects() -> list[ts.Project]:
    """
    Get all projects available to be filled in the timesheet
    :return: List of projects
    """
    projects = ts_client.get_projects()
    return projects

@app.tool()
def get_activities(project_id: int) -> list[ts.Activity]:
    """
    Get all activities available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of activities
    """
    activities = ts_client.get_activities(project_id)
    return activities


@app.tool()
def get_issues(project_id: int) -> list[ts.Issue]:
    """
    Get all issues available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of issues
    """
    issues = ts_client.get_issues(project_id)
    return issues

@app.tool()
def get_timesheets(start_date: str, end_date: str) -> list[ts.TimesheetEntry]:
    """
    Get all timesheet entries for a specific date range. The date format is YYYY-MM-DD.
    :param start_date: Start date of the timesheet
    :param end_date: End date of the timesheet
    :return: List of timesheet entries
    """
    timesheets = ts_client.get_timesheets(start_date, end_date)
    return timesheets

@app.tool()
def add_timesheet(
        project_id: int,
        activity_id: int,
        date: str, 
        hours: float, 
        description: str,
        issue_id: int | None = None) -> ts.TimesheetEntry:
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
    timesheet = ts_client.add_timesheet(project_id, activity_id, date, hours, description, issue_id)
    return timesheet

@app.tool()
def store_output(output: str, file_name: str) -> str:
    """
    Store text output into a file.
    :param output: Text output to be stored
    :param file_name: Name of the file to store the output
    """
    try:
        # Ensure the directory exists
        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        with open(f"{cfg.OUTPUT_DIR}/{file_name}", "w") as f:
            f.write(output)
        return f"Output stored as {file_name}"
    except Exception as e:
        return f"Error storing output: {str(e)}"
