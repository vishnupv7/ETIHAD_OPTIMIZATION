import requests
import pandas as pd

# Replace with your API Keys
OPENSKY_USERNAME = "your_opensky_username"
OPENSKY_PASSWORD = "your_opensky_password"
OPENWEATHER_API_KEY = "your_openweather_api_key"

# ✅ Fetch Live Flights (from OpenSky Public API)
def fetch_live_flights():
    try:
        url = "https://opensky-network.org/api/states/all"
        r = requests.get(url, timeout=15)
        data = r.json()
        if "states" not in data or not data["states"]:
            return pd.DataFrame()

        df = pd.DataFrame(data["states"], columns=[
            'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
            'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
            'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk',
            'spi', 'position_source'
        ])

        # ✅ Filter only Etihad flights (callsign starts with "ETD")
        etd_df = df[df['callsign'].astype(str).str.startswith('ETD')]
        return etd_df.reset_index(drop=True)
    except Exception as e:
        print(f"⚠️ Failed to fetch live flights: {e}")
        return pd.DataFrame()

# ✅ Fetch Live Weather (from OpenWeather API)
def fetch_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=10)
        data = r.json()
        return {
            "wind_speed_kt": data.get("wind", {}).get("speed", 0) * 1.94384,  # convert m/s to knots
            "pressure_hpa": data.get("main", {}).get("pressure", 1013),
            "temperature_c": data.get("main", {}).get("temp", 25)
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch weather: {e}")
        return {
            "wind_speed_kt": 10,   # Assume light wind if API fails
            "pressure_hpa": 1013,
            "temperature_c": 25
        }
