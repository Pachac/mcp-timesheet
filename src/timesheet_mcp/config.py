from dotenv import load_dotenv
import os

load_dotenv()

TS_PW = os.getenv("TIMESHEET_PASSWORD")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")