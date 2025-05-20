from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerStdio, MCPServer
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def run_agent(mcp_server: MCPServer):
    agent = Agent(
        name="Timesheet Agent",
        instructions="You are a timesheet management assistant. You can help me with timesheet-related tasks using available tools.",
        mcp_servers=[mcp_server],
        )
    test = await Runner.run(starting_agent=agent, input="Summarize the timesheet entries for this week (2025-05-19 - 2025-05-23).")
    print(test.final_output)


async def main():
    async with MCPServerStdio(
        params= {
            "command": "poetry",
            "args": ["run", "mcp", "run", "src/timesheet_mcp/server.py"],
            "env": {
                "TIMESHEET_PASSWORD": os.getenv("TIMESHEET_PASSWORD"),
            },
        },
        cache_tools_list=True,
        name="Timesheet MCP Server",
    ) as timesheet_server:
        trace_id = gen_trace_id()
        with trace(trace_id=trace_id, workflow_name="Timesheet MCP Server"):
            print(f"Starting Timesheet MCP Server with trace ID: {trace_id}")
            await run_agent(timesheet_server)

if __name__ == "__main__":
    asyncio.run(main())