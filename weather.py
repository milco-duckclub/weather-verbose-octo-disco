import requests
import datetime
import csv

def get_historical_weather(lat, lon, dt, api_key):
    """
    Retrieves historical weather data for a given location and time using the OpenWeatherMap One Call 3.0 API.

    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        dt: Unix timestamp for the desired date and time.
        api_key: Your OpenWeatherMap API key.

    Returns:
        A dictionary containing the historical weather data, or None if an error occurs.
    """

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&dt={dt}&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None  # Indicate that an error occurred

# Replace with your actual API key
api_key = "ad9ac0c2559cd138636ecf7217cf2917"  # Make sure to replace this with your actual API key

# Coordinates
lat = 38.1105
lon = -122.0945

# Get today's date
today = datetime.date.today()

# Calculate the date 300 days ago
start_date = today - datetime.timedelta(days=300)

# Open the CSV file for writing
with open('weather_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['date', 'temperature', 'feels_like', 'humidity', 'wind_speed', 'wind_deg', 'clouds'])  # Add more columns as needed

    # Loop through each day in the last 300 days
    for i in range(300):
        # Calculate the date for this iteration
        current_date = start_date + datetime.timedelta(days=i)

        # Determine the correct time zone (PDT or PST) based on the date
        if current_date.month in [11, 12, 1, 2]:  # November to February -> PST
            tzinfo = datetime.timezone(datetime.timedelta(hours=-8))
        else:  # March to October -> PDT
            tzinfo = datetime.timezone(datetime.timedelta(hours=-7))

        # Target time (16:00 in the determined time zone)
        target_datetime = datetime.datetime(current_date.year, current_date.month, current_date.day, 16, 0, 0, tzinfo=tzinfo)

        # Convert to Unix timestamp
        unix_timestamp = int(target_datetime.timestamp())

        # Get the historical weather data
        weather_data = get_historical_weather(lat, lon, unix_timestamp, api_key)

        # Check if weather data was fetched successfully
        if weather_data:
            # Extract relevant data 
            daily_data = weather_data.get('daily', [{}])[0] # Access the first item in the 'daily' list, if it exists
            temp = daily_data.get('temp', {}).get('day')  # Safely access nested values
            feels_like = daily_data.get('feels_like', {}).get('day')
            humidity = daily_data.get('humidity')
            wind_speed = daily_data.get('wind_speed')
            wind_deg = daily_data.get('wind_deg')
            clouds = daily_data.get('clouds')

            # Write the data to the CSV file
            writer.writerow([current_date, temp, feels_like, humidity, wind_speed, wind_deg, clouds]) 
        else:
            print(f"Skipping data for {current_date} due to error.")


            