import streamlit as st
import requests
from geopy.geocoders import Nominatim
import time

# 🔐 Your WeatherAPI Key
API_KEY = "0af6240444ce4b338ee84240251007"

# Configure Streamlit page
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Animated Background Elements */
    .background-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .cloud {
        position: absolute;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50px;
        animation: float 25s infinite linear;
    }
    
    .cloud:before {
        content: '';
        position: absolute;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50px;
    }
    
    .cloud1 {
        width: 80px;
        height: 30px;
        top: 15%;
        left: -80px;
    }
    
    .cloud1:before {
        width: 40px;
        height: 40px;
        top: -20px;
        left: 10px;
    }
    
    .cloud2 {
        width: 60px;
        height: 25px;
        top: 60%;
        left: -60px;
        animation-delay: -10s;
    }
    
    .cloud2:before {
        width: 30px;
        height: 30px;
        top: -15px;
        left: 15px;
    }
    
    @keyframes float {
        0% { transform: translateX(0); }
        100% { transform: translateX(calc(100vw + 100px)); }
    }
    
    /* Main Title */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
        animation: slideDown 1s ease-out;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        animation: slideDown 1s ease-out 0.3s both;
    }
    
    /* Weather Card */
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        animation: fadeIn 1s ease-out;
    }
    
    /* Weather Icon */
    .weather-icon {
        font-size: 8rem;
        text-align: center;
        animation: bounce 2s infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    
    /* Temperature Display */
    .temperature {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        text-align: center;
        margin: 0;
    }
    
    .condition {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Detail Cards */
    .detail-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .detail-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .detail-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .detail-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .detail-value {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Location Info */
    .location-info {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    .location-name {
        font-size: 1.5rem;
        color: solid black;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        height: 10px;
        background: solid black;
        border: none;
        border-radius: 50px;
        padding: 15px 20px;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        margin-top: -15px;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Animations */
    @keyframes slideDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.3);
        border-radius: 15px;
    }
    
    .stError {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 15px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .weather-icon {
            font-size: 5rem;
        }
        
        .temperature {
            font-size: 3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add animated background
st.markdown("""
<div class="background-animation">
    <div class="cloud cloud1"></div>
    <div class="cloud cloud2"></div>
</div>
""", unsafe_allow_html=True)

# 📍 Get coordinates from location
def get_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="smart-krishi-weather")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None, None
    return None, None

# 🌦️ Fetch weather from WeatherAPI
def get_weather(location_name):
    lat, lon = get_coordinates(location_name)
    if not lat:
        return None, "⚠️ Location not found. Try another city, village, or PIN."

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}&aqi=yes"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"⚠️ Weather API error: {response.status_code}"

        data = response.json()
        current = data['current']
        location_data = data['location']
        condition_text = current['condition']['text']
        emoji = weather_emoji(condition_text)

        weather_data = {
            "emoji": emoji,
            "condition": condition_text,
            "temp": current['temp_c'],
            "feels_like": current['feelslike_c'],
            "humidity": current['humidity'],
            "wind": current['wind_kph'],
            "aqi": current.get('air_quality', {}).get('pm2_5', 'N/A'),
            "location": f"{location_data['name']}, {location_data['country']}"
        }

        return weather_data, None
    except Exception as e:
        return None, f"⚠️ Failed to retrieve weather: {e}"

# 🌈 Emoji mapper
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

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-title">🌾 Smart Krishi Weather</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Live Weather Forecast with Beautiful Animations</p>', unsafe_allow_html=True)
    
    # Search Section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        location = st.text_input("📍 Enter location", "523001", label_visibility="collapsed", placeholder="Enter village name, city, or PIN code...")
    
    with col2:
        search_button = st.button("🔍 Get Weather", key="search")
    
    # Weather Display
    if search_button or location:
        if location:
            with st.spinner("🔍 Fetching weather data..."):
                weather, error = get_weather(location)
            
            if error:
                st.error(error)
            elif weather:
                # Weather Card
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                
                # Main Weather Display
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f'<div class="weather-icon">{weather["emoji"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'<div class="temperature">{weather["temp"]:.0f}°C</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="condition">{weather["condition"]}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Weather Details
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">💧</div>
                        <div class="detail-label">Humidity</div>
                        <div class="detail-value">{weather["humidity"]}%</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">💨</div>
                        <div class="detail-label">Wind Speed</div>
                        <div class="detail-value">{weather["wind"]} km/h</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">🌿</div>
                        <div class="detail-label">Air Quality</div>
                        <div class="detail-value">{weather["aqi"] if weather["aqi"] != "N/A" else "N/A"}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">🌡️</div>
                        <div class="detail-label">Feels Like</div>
                        <div class="detail-value">{weather["feels_like"]:.0f}°C</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Location Info
                st.markdown(f'''
                <div class="location-info">
                    <div class="location-name">📍 {weather["location"]}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Please enter a location to get weather information.")

if __name__ == "__main__":
    main()
