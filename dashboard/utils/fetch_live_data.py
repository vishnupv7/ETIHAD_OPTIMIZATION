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
def fetch_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    data = r.json()
    return {
        "wind_speed": data.get("wind", {}).get("speed", 10),
        "wind_deg": data.get("wind", {}).get("deg", 0),
        "pressure": data.get("main", {}).get("pressure", 1013),
        "temperature": data.get("main", {}).get("temp", 25)
    }
