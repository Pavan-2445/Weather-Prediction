# weather_app.py

import streamlit as st
from utils.weather import get_weather

st.set_page_config(page_title="🌦️ Live Weather Forecast", layout="centered")
st.title("🌍 Smart Krishi Assistant – Weather Forecast")

st.markdown("Enter a location to get the live weather report with beautiful emojis!")

location = st.text_input("📍 Enter location (city, district, or village)", "Hyderabad")

if location:
    with st.spinner("Fetching weather..."):
        weather_report = get_weather(location)
        st.markdown(weather_report)
