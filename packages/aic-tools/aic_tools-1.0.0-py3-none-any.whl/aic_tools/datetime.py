from crewai_tools import tool
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@tool("Check date/time")
def get_datetime(timezone: str) -> str:
    """Returns current datetime in timezone."""
    try:
        timezone = ZoneInfo(timezone)
        now = datetime.now(timezone)
        return now.strftime('%Y-%m-%d %H:%M:%S')
    except ZoneInfoNotFoundError:
        return "Unknown timezone"