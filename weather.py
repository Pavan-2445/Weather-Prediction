import requests
from geopy.geocoders import Nominatim

API_KEY = "YOUR_API"  # Replace with your actual API key

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="smart-krishi-weather")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_weather(location_name):
    lat, lon = get_coordinates(location_name)
    if not lat:
        return "⚠️ Location not found. Please enter a valid city, district, or village."

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    response = requests.get(url)
    if response.status_code != 200:
        return "⚠️ Weather API error"

    data = response.json()
    current = data['current']
    emoji = weather_emoji(current['condition']['text'])

    weather_info = f"""
    ## {emoji} {current['condition']['text']}
    - 🌡️ Temperature: **{current['temp_c']}°C**
    - 💧 Humidity: **{current['humidity']}%**
    - 💨 Wind Speed: **{current['wind_kph']} km/h**
    """

    return weather_info

def weather_emoji(condition):
    condition = condition.lower()
    if 'sunny' in condition or 'clear' in condition:
        return "☀️"
    elif 'cloud' in condition:
        return "☁️"
    elif 'rain' in condition:
        return "🌧️"
    elif 'thunder' in condition:
        return "⛈️"
    elif 'snow' in condition:
        return "❄️"
    elif 'fog' in condition or 'mist' in condition:
        return "🌫️"
    else:
        return "🌈"
