from timesheet import TimesheetClient
from config import TS_PW

client = TimesheetClient(
    username="tomas.pachovsky",
    password=TS_PW
)

client.add_timesheet(
  project_id= 6356,
  activity_id= 9,
  date= "2025-05-20",
  hours= 2,
  issue_id=57166,
  description= "Development work on Grohe Neo project"
)