import requests
import pandas as pd
import matplotlib.pyplot as plt
from .location import get_location_from_ip
from datetime import date, timedelta


class WeatherData:
    def __init__(self) -> None:
        self.location = get_location_from_ip()
        self.latitute = self.location.get("latitude")
        self.longitude = self.location.get("longitude")
        self.weather_data = None

    def get_elevation_by_location(self) -> dict:
        elevation_url = (
            f"https://api.open-meteo.com/v1/elevation"
            f"?latitude={self.latitute}&longitude={self.longitude}"
        )
        res = requests.get(elevation_url).json()

        if 'elevation' not in res:
            return {"error": "Elevation data not available for the given location."}

        return res

    def get_weather_by_location(self) -> pd.DataFrame:
        if "error" in self.location:
            return pd.DataFrame({"error": "Could not determine location from IP address."})

        start_day_str = date.today().strftime("%Y-%m-%d")
        end_day = date.today() + timedelta(weeks=1)
        end_day_str = end_day.strftime("%Y-%m-%d")

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.latitute}&longitude={self.longitude}"
            f"&hourly=visibility,precipitation_probability,cloud_cover,relative_humidity_2m"
            f"&timezone=auto"
            f"&start_date={start_day_str}&end_date={end_day_str}"
        )

        res = requests.get(weather_url).json()

        if 'hourly' not in res:
            return pd.DataFrame({"error": "Weather data not available for the given location."})

        hourly_data = res['hourly']
        self.weather_data = pd.DataFrame(hourly_data)
        self.weather_data.set_index('time', inplace=True)
        self.weather_data.index.name = "time"
        return self.weather_data

    def plot_weather_data(self) -> None:
        if self.weather_data is None:
            print("NO DATA to PLOT")
            return

        normalized_weather_data = (
            self.weather_data - self.weather_data.mean()) / self.weather_data.std()
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
