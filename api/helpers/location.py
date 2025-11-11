import requests
from geopy.geocoders import Nominatim
from datetime import datetime


def get_current_datetime() -> str:
    """Return the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_coordinates(location: str) -> tuple:
    """Get coordinates based on user input location."""
    # geolocator = Nominatim(user_agent="stargazing_app")
    # loc = geolocator.geocode(location)
    # if not loc:
    #     raise ValueError(f"Location '{location}' not found.")
    # return loc.latitude, loc.longitude
    return ()


def get_location_from_ip() -> dict:
    """Get the geographical location based on the IP address."""
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        if 'loc' in data:
            latitude, longitude = data['loc'].split(',')
            data = {
                "latitude": latitude,
                "longitude": longitude,
                "city": data.get('city', 'N/A'),
                "country": data.get('country', 'N/A'),
            }
            return data
        else:
            return {"error": "Location data not found in response."}
    except Exception as e:
        return {"error": f"Error occurred: {e}"}
