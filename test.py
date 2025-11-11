from api.helpers.weather import WeatherData
from api.helpers.location import get_location_from_ip

weather_object = WeatherData()
print(weather_object.get_elevation_by_location())
# print(weather_object.get_weather_by_location())
weather_outcome = weather_object.get_weather_by_location()
print(weather_outcome.to_string())
# print(weather_object.plot_weather_data())
