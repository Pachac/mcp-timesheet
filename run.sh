#!/usr/bin/env bash
# run.sh
cd /home/tomas/repositories/mcp-timesheet
exec poetry run mcp run src/timesheet_mcp/server.py
