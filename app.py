import streamlit as st
import requests
from geopy.geocoders import Nominatim
import time
import os
from dotenv import load_dotenv
from gtts import gTTS
import base64
import io



# 🔐 Your WeatherAPI Key
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# Configure Streamlit page
st.set_page_config(
    page_title="Weather Speak",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced language translations with detailed weather reports
translations = {
    "en": {
        "title": "🌦️ Weather Speak 🗣",
        "subtitle": "Live Weather Forecast with Beautiful Animations",
        "input_placeholder": "Enter village name, city, or PIN code...",
        "button_text": "🔍 Get Weather",
        "loading": "🔍 Fetching weather data...",
        "location_error": "⚠️ Location not found. Try another city, village, or PIN.",
        "api_error": "⚠️ Weather API error: {}",
        "weather_error": "⚠️ Failed to retrieve weather: {}",
        "enter_location": "Please enter a location to get weather information.",
        "labels": {
            "humidity": "Humidity",
            "wind": "Wind Speed",
            "air_quality": "Air Quality",
            "feels_like": "Feels Like",
            "condition": "Condition",
            "temperature": "Temperature"
        },
        "weather_report": {
            "intro": "Here's the detailed weather report for {}",
            "temp": "The current temperature is {:.0f} degrees Celsius",
            "feels_like": "but it feels like {:.0f} degrees",
            "condition": "with {} conditions",
            "humidity": "Humidity is at {} percent",
            "wind": "and wind speeds of {} kilometers per hour",
            "air_quality": "Air quality index shows {} micrograms per cubic meter of PM2.5"
        }
    },
    "te": {
        "title": "🌦️ వాతావరణ స్పీక్ 🗣",
        "subtitle": "అందమైన యానిమేషన్లతో ప్రత్యక్ష వాతావరణ సూచన",
        "input_placeholder": "గ్రామం పేరు, నగరం లేదా పిన్ కోడ్ నమోదు చేయండి...",
        "button_text": "🔍 వాతావరణ పొందండి",
        "loading": "🔍 వాతావరణ డేటా తెస్తున్నాము...",
        "location_error": "⚠️ స్థానం కనుగొనబడలేదు. మరొక నగరం, గ్రామం లేదా పిన్ ప్రయత్నించండి.",
        "api_error": "⚠️ వాతావరణ API లోపం: {}",
        "weather_error": "⚠️ వాతావరణ పొందడంలో విఫలమైంది: {}",
        "enter_location": "వాతావరణ సమాచారం పొందడానికి దయచేసి స్థానాన్ని నమోదు చేయండి.",
        "labels": {
            "humidity": "తేమ",
            "wind": "గాలి వేగం",
            "air_quality": "గాలి నాణ్యత",
            "feels_like": "అనుభూతి",
            "condition": "స్థితి",
            "temperature": "ఉష్ణోగ్రత"
        },
        "weather_report": {
            "intro": "{} కోసం వివరణాత్మక వాతావరణ నివేదిక ఇది",
            "temp": "ప్రస్తుత ఉష్ణోగ్రత {:.0f} డిగ్రీల సెల్సియస్",
            "feels_like": "కానీ {:.0f} డిగ్రీలుగా అనిపిస్తుంది",
            "condition": "{} పరిస్థితులతో",
            "humidity": "తేమ {} శాతం ఉంది",
            "wind": "మరియు గంటకు {} కిలోమీటర్ల వేగంతో గాలి వీస్తోంది",
            "air_quality": "గాలి నాణ్యత సూచిక PM2.5 కు {} మైక్రోగ్రాములు ప్రతి క్యూబిక్ మీటరుకు చూపిస్తుంది"
        }
    },
    "hi": {
        "title": "🌦️ मौसम स्पीक 🗣",
        "subtitle": "सुंदर एनिमेशन के साथ लाइव मौसम पूर्वानुमान",
        "input_placeholder": "गाँव का नाम, शहर या पिन कोड दर्ज करें...",
        "button_text": "🔍 मौसम प्राप्त करें",
        "loading": "🔍 मौसम डेटा प्राप्त कर रहे हैं...",
        "location_error": "⚠️ स्थान नहीं मिला। किसी अन्य शहर, गाँव या पिन को आज़माएँ।",
        "api_error": "⚠️ मौसम API त्रुटि: {}",
        "weather_error": "⚠️ मौसम प्राप्त करने में विफल: {}",
        "enter_location": "मौसम की जानकारी प्राप्त करने के लिए कृपया स्थान दर्ज करें।",
        "labels": {
            "humidity": "नमी",
            "wind": "हवा की गति",
            "air_quality": "वायु गुणवत्ता",
            "feels_like": "अनुभूति",
            "condition": "स्थिति",
            "temperature": "तापमान"
        },
        "weather_report": {
            "intro": "{} के लिए विस्तृत मौसम रिपोर्ट यहां है",
            "temp": "वर्तमान तापमान {:.0f} डिग्री सेल्सियस है",
            "feels_like": "लेकिन यह {:.0f} डिग्री जैसा महसूस होता है",
            "condition": "{} स्थितियों के साथ",
            "humidity": "नमी {} प्रतिशत है",
            "wind": "और हवा की गति {} किलोमीटर प्रति घंटा है",
            "air_quality": "वायु गुणवत्ता सूचकांक PM2.5 के लिए {} माइक्रोग्राम प्रति घन मीटर दिखाता है"
        }
    }
}

# Weather condition translations
condition_translations = {
    "en": {
        "Sunny": "sunny",
        "Clear": "clear",
        "Partly cloudy": "partly cloudy",
        "Cloudy": "cloudy",
        "Overcast": "overcast",
        "Mist": "misty",
        "Fog": "foggy",
        "Light rain": "light rain",
        "Moderate rain": "moderate rain",
        "Heavy rain": "heavy rain",
        "Thunderstorm": "thunderstorms",
        "Snow": "snow",
        "Haze": "haze"
    },
    "te": {
        "Sunny": "ఎండ",
        "Clear": "స్పష్టంగా",
        "Partly cloudy": "పాక్షికంగా మేఘావృతం",
        "Cloudy": "మేఘావృతం",
        "Overcast": "గుడ్డు మబ్బు",
        "Mist": "పొగమంచు",
        "Fog": "మంచు",
        "Light rain": "తేలికపాటి వర్షం",
        "Moderate rain": "మధ్యస్థ వర్షం",
        "Heavy rain": "భారీ వర్షం",
        "Thunderstorm": "గాలి వాన",
        "Snow": "హిమపాతం",
        "Haze": "మసక"
    },
    "hi": {
        "Sunny": "धूप",
        "Clear": "साफ",
        "Partly cloudy": "आंशिक रूप से बादल",
        "Cloudy": "बादल",
        "Overcast": "घटाटोप",
        "Mist": "धुंध",
        "Fog": "कोहरा",
        "Light rain": "हल्की बारिश",
        "Moderate rain": "मध्यम बारिश",
        "Heavy rain": "भारी बारिश",
        "Thunderstorm": "आंधी तूफान",
        "Snow": "बर्फ",
        "Haze": "धुंध"
    }
}

# [Previous CSS code remains exactly the same...]

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
        height: 20px;
        background: solid black;
        border: none;
        border-radius: 50px;
        padding: 15px 20px;
        font-size: 1.8rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        margin-top: -15px;
        padding: 15px 30px;
        font-size: 1.8rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Language Toggle */
    .language-toggle {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    
    .language-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        border-radius: 50px;
        padding: 8px 15px;
        margin: 0 5px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .language-btn:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    .language-btn.active {
        background: rgba(255, 255, 255, 0.4);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
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
        
        .language-toggle {
            top: 10px;
            right: 10px;
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

# Function to create audio autoplay
def autoplay_audio(audio_file):
    audio_file.seek(0)
    data = audio_file.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay controls">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.querySelector("audio");
            if (audio) {{
                audio.play().catch(e => {{
                    console.warn("Autoplay blocked");
                }});
            }}
        </script>
    """
    st.markdown(md, unsafe_allow_html=True)

# Function to generate speech from text with fallback
def text_to_speech(text, lang):
    try:
        lang_code = {"en": "en", "te": "te", "hi": "hi"}.get(lang, "en")
        tts = gTTS(text=text, lang=lang_code)
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    except Exception as e:
        st.error(f"gTTS failed: {e}")
        return None


# Function to generate detailed weather report text
def generate_weather_report(weather_data, lang):
    t = translations[lang]
    cond_t = condition_translations[lang]
    report = t["weather_report"]
    
    translated_condition = cond_t.get(weather_data["condition"], weather_data["condition"])
    
    report_text = "\n".join([
        report["intro"].format(weather_data["location"]),
        report["temp"].format(weather_data["temp"]),
        report["feels_like"].format(weather_data["feels_like"]),
        report["condition"].format(translated_condition),
        report["humidity"].format(weather_data["humidity"]),
        report["wind"].format(weather_data["wind"]),
        report["air_quality"].format(weather_data["aqi"]) if weather_data["aqi"] != "N/A" else ""
    ])
    
    return report_text

# Main App
def main():
    # Step 1: Language Selection UI (Streamlit-native)
    lang_options = {
        "English": "en",
        "हिंदी": "hi",
        "తెలుగు": "te"
    }

    # Ensure consistent state for selected language
    if 'lang' not in st.session_state:
        st.session_state.lang = "en"

    lang_display = st.selectbox(
        "🌐 Choose Language",
        list(lang_options.keys()),
        index=list(lang_options.values()).index(st.session_state.get("lang", "en")))
    st.session_state.lang = lang_options[lang_display]

    # Step 2: Load translations
    lang = st.session_state.lang
    t = translations[lang]
    cond_t = condition_translations[lang]

    # Header
    st.markdown(f'<h1 class="main-title">{t["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

    # Search Section
    col1, col2 = st.columns([3, 1])

    with col1:
        location = st.text_input("📍", "523001", label_visibility="collapsed", placeholder=t["input_placeholder"])

    with col2:
        search_button = st.button(t["button_text"], key="search")

    # Weather Display
    if search_button or location:
        if location:
            with st.spinner(t["loading"]):
                weather, error = get_weather(location)

            if error:
                st.error(error)
            elif weather:
                # Generate detailed weather report text
                report_text = generate_weather_report(weather, lang)
                
                # TTS in selected language
                audio_file = text_to_speech(report_text, lang)
                if audio_file:
                    autoplay_audio(audio_file)
                
                # Display weather information
                translated_condition = cond_t.get(weather["condition"], weather["condition"])
                
                # Weather Card
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f'<div class="weather-icon">{weather["emoji"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="temperature">{weather["temp"]:.0f}°C</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="condition">{translated_condition}</div>', unsafe_allow_html=True)

                st.markdown("---")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">💧</div>
                        <div class="detail-label">{t["labels"]["humidity"]}</div>
                        <div class="detail-value">{weather["humidity"]}%</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">💨</div>
                        <div class="detail-label">{t["labels"]["wind"]}</div>
                        <div class="detail-value">{weather["wind"]} km/h</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col3:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">🌿</div>
                        <div class="detail-label">{t["labels"]["air_quality"]}</div>
                        <div class="detail-value">{weather["aqi"] if weather["aqi"] != "N/A" else "N/A"}</div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col4:
                    st.markdown(f'''
                    <div class="detail-card">
                        <div class="detail-icon">🌡️</div>
                        <div class="detail-label">{t["labels"]["feels_like"]}</div>
                        <div class="detail-value">{weather["feels_like"]:.0f}°C</div>
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown(f'''
                <div class="location-info">
                    <div class="location-name">📍 {weather["location"]}</div>
                </div>
                ''', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(t["enter_location"])
if __name__ == "__main__":
    main()
