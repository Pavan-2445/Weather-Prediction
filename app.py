import streamlit as st
import requests
from geopy.geocoders import Nominatim

# 🔐 WeatherAPI Key
API_KEY = "0af6240444ce4b338ee84240251007"  # ✅ Replace with your actual key

# 📍 Get coordinates
def get_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="smart-krishi-weather")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None, None
    return None, None

# 🌦️ Get weather from WeatherAPI
def get_weather(location_name):
    lat, lon = get_coordinates(location_name)
    if not lat:
        return None, "⚠️ Location not found. Try a nearby city or valid PIN code."

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"⚠️ Weather API error: {response.status_code} – {response.text}"

        data = response.json()
        current = data['current']
        condition_text = current['condition']['text']
        emoji = weather_emoji(condition_text)

        weather_data = {
            "emoji": emoji,
            "condition": condition_text,
            "temp": current['temp_c'],
            "humidity": current['humidity'],
            "wind": current['wind_kph'],
            "aqi": current.get('air_quality', {}).get('pm2_5', 'N/A'),  # Optional AQI
            "location": location_name.title()
        }

        return weather_data, None
    except Exception as e:
        return None, f"⚠️ Failed to retrieve weather: {e}"

# 🌈 Better emoji mapper
def weather_emoji(condition):
    condition = condition.lower()
    if 'sunny' in condition or 'clear' in condition:
        return "☀️"
    elif 'partly cloudy' in condition:
        return "⛅"
    elif 'overcast' in condition:
        return "🌥️"
    elif 'cloud' in condition:
        return "☁️"
    elif 'rain' in condition or 'drizzle' in condition:
        return "🌧️"
    elif 'thunder' in condition:
        return "⛈️"
    elif 'snow' in condition:
        return "❄️"
    elif 'fog' in condition or 'mist' in condition or 'haze' in condition:
        return "🌫️"
    else:
        return "🌈"

# 🌤️ Streamlit UI
st.set_page_config(page_title="🌦️ Weather Forecast", layout="centered")
st.title("🌾 Smart Krishi Assistant – Live Weather")
st.markdown("Enter a city, village, or PIN code to get live weather updates with enriched visuals and AQI 🍃")

# 📍 Input location
location = st.text_input("📍 Location", "523001")

if location:
    with st.spinner("🔍 Fetching weather..."):
        weather, error = get_weather(location)

    if error:
        st.error(error)
    elif weather:
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(f"<div style='font-size:100px; text-align:center;'>{weather['emoji']}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                ### 🌤️ Condition: **{weather['condition']}**
                - 🌡️ **Temperature**: {weather['temp']}°C  
                - 💧 **Humidity**: {weather['humidity']}%  
                - 💨 **Wind Speed**: {weather['wind']} km/h  
                - 🌿 **Air Quality Index (PM2.5)**: {weather['aqi']}  
                - 📍 **Location**: {weather['location']}
            """)
