from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("TIMESHEET_USERNAME")
PW = os.getenv("TIMESHEET_PASSWORD")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://timesheet.actum.cz/api")