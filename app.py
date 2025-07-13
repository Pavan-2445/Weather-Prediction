import streamlit as st
import streamlit.components.v1 as components
import requests

# 🔐 Weather API
API_KEY = "0af6240444ce4b338ee84240251007"

# 🌦️ Get weather by coordinates
def get_weather(lat, lon):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"
    response = requests.get(url)
    if response.status_code != 200:
        return "⚠️ Weather API error"
    
    data = response.json()
    current = data['current']
    emoji = weather_emoji(current['condition']['text'])

    return f"""
    ## {emoji} {current['condition']['text']}
    - 🌡️ Temp: **{current['temp_c']}°C**
    - 💧 Humidity: **{current['humidity']}%**
    - 💨 Wind: **{current['wind_kph']} km/h**
    """

# 🌈 Emoji Helper
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

# UI
st.set_page_config(page_title="📍Weather by My Location", layout="centered")
st.title("📍 Live Weather at Your Current Location")

# 🌍 Inject JavaScript to get browser's location
components.html(
    """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = `/get_location?lat=${lat}&lon=${lon}`;
            document.body.appendChild(iframe);
        },
        (error) => {
            alert('Location access denied.');
        }
    );
    </script>
    """,
    height=0,
)

# 💡 Get values from query params
query_params = st.experimental_get_query_params()

if "lat" in query_params and "lon" in query_params:
    lat = query_params["lat"][0]
    lon = query_params["lon"][0]
    weather = get_weather(lat, lon)
    st.markdown(weather)
else:
    st.info("🔍 Waiting for geolocation permission from browser...")
