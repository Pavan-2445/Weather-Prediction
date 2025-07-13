import streamlit as st
import requests
from geopy.geocoders import Nominatim

# 🔐 Set your WeatherAPI key here
API_KEY = "0af6240444ce4b338ee84240251007"  # ⬅️ Replace this with your actual key

# 🌍 Convert any location name or PIN to coordinates
def get_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="smart-krishi-weather")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        return None, None
    return None, None

# 🌦️ Fetch weather from WeatherAPI using coordinates
def get_weather(location_name):
    lat, lon = get_coordinates(location_name)
    if not lat:
        return "⚠️ Location not found. Please enter a valid village, city, or PIN code."

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"⚠️ Weather API error: {response.status_code} – {response.text}"

        data = response.json()
        current = data['current']
        emoji = weather_emoji(current['condition']['text'])

        return f"""
        ## {emoji} {current['condition']['text']}
        - 🌡️ Temperature: **{current['temp_c']}°C**
        - 💧 Humidity: **{current['humidity']}%**
        - 💨 Wind Speed: **{current['wind_kph']} km/h**
        - 📍 Location: **{location_name.title()}**
        """
    except Exception as e:
        return f"⚠️ Failed to retrieve weather: {e}"

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

# 🌤️ Streamlit UI
st.set_page_config(page_title="🌦️ Live Weather Forecast", layout="centered")
st.title("🌍 Smart Krishi Assistant – Weather Forecast")
st.markdown("Enter a village name, city, or PIN code to get real-time weather updates! 🛰️")

# 🧾 User input
location = st.text_input("📍 Enter location", "523001")  # Default PIN code or city

if location:
    with st.spinner("Fetching weather..."):
        weather_report = get_weather(location)
        st.markdown(weather_report)
