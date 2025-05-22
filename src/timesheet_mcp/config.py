from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("TIMESHEET_USERNAME", "tomas.pachovsky")
PW = os.getenv("TIMESHEET_PASSWORD")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")