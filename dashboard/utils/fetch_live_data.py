import requests
import pandas as pd

OPENSKY_USERNAME = "23154040424@manipalacademyonline.edu.in"
OPENSKY_PASSWORD = "@jHmyb5LhN52MiK"
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

def fetch_live_flights():
    url = "https://opensky-network.org/api/states/all"
    r = requests.get(url, auth=(OPENSKY_USERNAME, OPENSKY_PASSWORD))
    data = r.json()
    if not data.get("states"):
        return pd.DataFrame()
    
    df = pd.DataFrame(data['states'], columns=[
        'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
        'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
        'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk',
        'spi', 'position_source'
    ])
    etd_df = df[df['callsign'].astype(str).str.startswith('ETD')]
    return etd_df

def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "wind_speed": data['wind']['speed'],
        "wind_deg": data['wind']['deg'],
        "pressure": data['main']['pressure'],
        "temperature": data['main']['temp']
    }