from datetime import date
from api.helpers.weather import get_elevation_by_location, get_weather_by_location
from api.helpers.location import get_location_from_ip, get_coordinates

# lat, longi = get_coordinates("Los Banos, California")
# print(get_elevation_by_location(lat, longi))
# # print(weather_object.get_weather_by_location())
loc = "Los Banos, California"
weather_outcome = get_weather_by_location(loc, date.today())
print(type(weather_outcome))
# # print(weather_outcome.to_string())
# # print(weather_object.plot_weather_data())
