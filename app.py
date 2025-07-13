import streamlit as st
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# 🔐 Add your actual WeatherAPI key here
API_KEY = "0af6240444ce4b338ee84240251007"  # ← Replace this now

# 🌍 Nominatim for geocoding
def get_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="smart-krishi-assistant-weather")
        location = geolocator.geocode(location_name, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None, None
    return None, None

# 🌦️ Get weather using WeatherAPI
def get_weather(location_name):
    lat, lon = get_coordinates(location_name)
    if not lat or not lon:
        return "⚠️ Location not found or Nominatim failed. Please try a nearby city or valid PIN."

    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"❌ WeatherAPI Error ({response.status_code}): {response.text}"

        data = response.json()
        current = data['current']
        emoji = weather_emoji(current['condition']['text'])

        return f"""
        ## {emoji} {current['condition']['text']}
        - 🌡️ Temp: **{current['temp_c']}°C**
        - 💧 Humidity: **{current['humidity']}%**
        - 💨 Wind: **{current['wind_kph']} km/h**
        - 📍 Location: **{location_name.title()}**
        """
    except Exception as e:
        return f"💥 Exception: {e}"

# 🌈 Emoji mapper
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

# 🚀 Streamlit App
st.set_page_config(page_title="🌦️ Live Weather Forecast", layout="centered")
st.title("🌍 Smart Krishi Assistant – Weather Forecast")
st.markdown("Enter a village name, city, or PIN code to get accurate weather updates using Nominatim & WeatherAPI.")

# 📍 Input location
location = st.text_input("📍 Enter location", "Hyderabad")

if location:
    with st.spinner("Fetching weather data..."):
        result = get_weather(location)
        st.markdown(result)
