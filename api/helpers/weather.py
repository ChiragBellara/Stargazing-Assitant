import requests
import pandas as pd
import matplotlib.pyplot as plt
from .location import get_coordinates
from datetime import date as DateType, timedelta


def get_elevation_by_location(latitude, longitude) -> dict:
    elevation_url = (
        f"https://api.open-meteo.com/v1/elevation"
        f"?latitude={latitude}&longitude={longitude}"
    )
    res = requests.get(elevation_url).json()

    if 'elevation' not in res:
        return {"error": "Elevation data not available for the given location."}

    return res


def get_weather_by_location(location: str, date: DateType) -> dict:

    latitude, longitude = get_coordinates(location)

    start_day_str = date.strftime("%Y-%m-%d")
    end_day = date + timedelta(weeks=1)
    end_day_str = end_day.strftime("%Y-%m-%d")

    all_data = get_elevation_by_location(latitude, longitude)

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&hourly=visibility,precipitation_probability,cloud_cover,relative_humidity_2m"
        f"&timezone=auto"
        f"&start_date={start_day_str}&end_date={end_day_str}"
    )

    res = requests.get(weather_url).json()

    if 'hourly' not in res:
        return {"error": "Weather data not available for the given location."}

    hourly_data = res['hourly']
    weather_data = pd.DataFrame(hourly_data)
    weather_data.set_index('time', inplace=True)
    weather_data.index.name = "time"

    all_data["weather_data"] = weather_data.to_dict()
    return all_data


def plot_weather_data(weather_data) -> None:
    if weather_data is None:
        print("NO DATA to PLOT")
        return

    normalized_weather_data = (
        weather_data - weather_data.mean()) / weather_data.std()
    plt.plot(
        normalized_weather_data.index, normalized_weather_data["visibility"], marker='o', label='Visibility')
    plt.plot(normalized_weather_data.index, normalized_weather_data["precipitation_probability"],
             marker='s', label='Precipitation Probs')
    plt.plot(
        normalized_weather_data.index, normalized_weather_data["cloud_cover"], marker='*', label='Cloud Cover')
    plt.plot(normalized_weather_data.index, normalized_weather_data["relative_humidity_2m"],
             marker='+', label='Relative Humidity')

    plt.xlabel("Location")
    plt.ylabel("Value")
    plt.title("Weather Values by Time")
    plt.legend()

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    return
