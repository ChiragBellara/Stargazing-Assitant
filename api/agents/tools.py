from langchain_community.tools import tool
from datetime import datetime
from helpers.weather import get_weather_by_location


@tool
def fetch_weather(location: str, date_str: str) -> dict | str:
    """Returns the weather summary for a given location for the next seven days starting today"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    data = get_weather_by_location(location, date)
    if data is None:
        return "Unable to fetch the weather data"
    return data

