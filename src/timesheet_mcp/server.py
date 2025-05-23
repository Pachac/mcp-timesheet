from mcp.server.fastmcp import FastMCP
import timesheet_mcp.timesheet as ts
import timesheet_mcp.models as models
import timesheet_mcp.config as cfg
import os

app = FastMCP(
    name="Timesheet",
    instructions="Timesheet Management System"
)
if cfg.TOKEN:
    ts_client = ts.TimesheetClient(
        token=cfg.TOKEN,
        base_url=cfg.BASE_URL,
    )
elif cfg.USERNAME and cfg.PW:
    ts_client = ts.TimesheetClient(
        username=cfg.USERNAME,
        password=cfg.PW,
        base_url=cfg.BASE_URL,
    )
else:
    raise ValueError("Either username/password or token must be provided.")

@app.tool()
def get_projects() -> list[models.Project]:
    """
    Get all projects available to be filled in the timesheet
    :return: List of projects
    """
    projects = ts_client.get_projects()
    return projects

@app.tool()
def get_activities(project_id: int) -> list[models.Activity]:
    """
    Get all activities available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of activities
    """
    activities = ts_client.get_activities(project_id)
    return activities


@app.tool()
def get_issues(project_id: int) -> list[models.Issue]:
    """
    Get all issues available to be filled in the timesheet for a specific project
    :param project_id: ID of the project
    :return: List of issues
    """
    issues = ts_client.get_issues(project_id)
    return issues

@app.tool()
def get_timesheets(start_date: str, end_date: str) -> list[models.TimesheetEntry]:
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
        comments: str,
        issue_id: int | None = None) -> list[models.TimesheetEntry]:
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
    entry = models.TimesheetEntryInput(
        project_id=project_id,
        activity_id=activity_id,
        date=date,
        hours=hours,
        comments=comments,
        issue_id=issue_id
    )
    timesheet = ts_client.add_timesheet_entry(entry)
    return timesheet

@app.tool()
def edit_timesheet(
        entry_id: int,
        project_id: int,
        activity_id: int,
        date: str, 
        hours: float, 
        comments: str,
        issue_id: int | None = None) -> str:
    """
    Edit a timesheet entry for a specific project, activity, and date. The date format is YYYY-MM-DD.
    :param entry_id: ID of the timesheet entry to be edited
    :param project_id: ID of the project
    :param activity_id: ID of the activity
    :param date: Date of the timesheet entry
    :param hours: Number of hours worked
    :param description: Description of the timesheet entry
    :param issue_id: ID of the issue (optional)
    :return: Edited timesheet entry
    """
    entry = models.TimesheetEntryInput(
        project_id=project_id,
        activity_id=activity_id,
        date=date,
        hours=hours,
        comments=comments,
        issue_id=issue_id
    )
    message = ts_client.edit_timesheet_entry(entry_id, entry)
    return message

@app.tool()
def delete_timesheet(entry_id: int) -> str:
    """
    Delete a timesheet entry by its ID.
    :param entry_id: ID of the timesheet entry to be deleted
    :return: Confirmation message
    """
    try:
        ts_client.delete_timesheet_entry(entry_id)
        return f"Timesheet entry with ID {entry_id} deleted successfully."
    except Exception as e:
        return f"Error deleting timesheet entry: {str(e)}"

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

def run():
    """
    Run the FastMCP server.
    """
    app.run()