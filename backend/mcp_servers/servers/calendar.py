import os
from mcp import StdioServerParameters


def get_calendar_server_params() -> StdioServerParameters:
    """Returns MCP server parameters for Google Calendar."""
    
    creds = os.getenv("GOOGLE_OAUTH_CREDENTIALS")
    if not creds:
        raise ValueError("GOOGLE_OAUTH_CREDENTIALS environment variable not set")
    
    return StdioServerParameters(
        command="npx",
        args=["-y", "@cocal/google-calendar-mcp"],
        env={"GOOGLE_OAUTH_CREDENTIALS": creds}
    )