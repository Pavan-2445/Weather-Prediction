import streamlit as st
import requests

API_KEY = "0af6240444ce4b338ee84240251007"  # ⬅️ Replace with your actual key

def get_weather(location_name):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location_name}"
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

# Streamlit UI
st.set_page_config(page_title="🌦️ Live Weather Forecast", layout="centered")
st.title("🌍 Smart Krishi Assistant – Weather Forecast")
st.markdown("Enter a village name, city, or PIN code to get real-time weather updates! 🛰️")

# Input
location = st.text_input("📍 Enter location", "Hyderabad")

if location:
    with st.spinner("Fetching weather..."):
        weather_report = get_weather(location)
        st.markdown(weather_report)
