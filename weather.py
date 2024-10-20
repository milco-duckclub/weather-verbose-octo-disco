import requests
import datetime

def get_historical_weather(lat, lon, dt, api_key):
  """
  Retrieves historical weather data for a given location and time using the OpenWeatherMap One Call 3.0 API.

  Args:
    lat: Latitude of the location.
    lon: Longitude of the location.
    dt: Unix timestamp for the desired date and time.
    api_key: Your OpenWeatherMap API key.

  Returns:
    A dictionary containing the historical weather data.
  """

  url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={api_key}"

  response = requests.get(url)
  response.raise_for_status()

  return response.json()

# Replace with your actual API key
api_key = "YOUR_API_KEY"

# LaFayette, California coordinates
lat = 37.8918
lon = -122.1239

# Target date and time (Friday, October 11th, 2024 at 11 AM PDT)
target_datetime = datetime.datetime(2024, 10, 11, 11, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-7)))  # PDT

# Convert to Unix timestamp
unix_timestamp = int(target_datetime.timestamp())

# Get the historical weather data
weather_data = get_historical_weather(lat, lon, unix_timestamp, api_key)

# Print the weather data
print(weather_data)
