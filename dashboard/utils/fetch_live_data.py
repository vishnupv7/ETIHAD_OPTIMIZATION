import requests
import pandas as pd

# OpenWeather API
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

def fetch_live_flights():
    """
    Fetch live Etihad flights (callsigns starting with 'ETD') from OpenSky Public REST API.
    """
    url = "https://opensky-network.org/api/states/all"
    try:
        r = requests.get(url, timeout=30)
        data = r.json()
        if "states" not in data or data["states"] is None:
            return pd.DataFrame()

        columns = [
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
            "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
            "spi", "position_source"
        ]
        df = pd.DataFrame(data["states"], columns=columns)
        df = df[df["callsign"].notna()]
        df["callsign"] = df["callsign"].str.strip()
        etd_df = df[df["callsign"].str.startswith("ETD")]

        return etd_df

    except Exception as e:
        print(f"⚠️ Error fetching flights: {e}")
        return pd.DataFrame()

def fetch_weather(lat, lon):
    """
    Fetch live weather from OpenWeather for given coordinates.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            return None
        data = r.json()
        return {
            "wind_speed_kt": data['wind']['speed'] * 1.94384 if 'wind' in data else None,
            "pressure_hpa": data['main']['pressure'] if 'main' in data else None,
            "temperature_c": data['main']['temp'] if 'main' in data else None
        }
    except Exception as e:
        print(f"⚠️ Error fetching weather: {e}")
        return None
    ''')
