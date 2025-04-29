

import requests

# 🚀 Updated to accept openweather key properly
def prepare_live_features(flight, openweather_api_key=None):
    features = {}
    
    # Extract available fields
    features['distance_km'] = 3000  # Placeholder because OpenSky does not give direct distance
    features['deviation_flag'] = 0
    features['expected_flight_duration_sec'] = 3600 * 6  # Assume 6 hours for now
    features['distance_penalty_km'] = 0

    # Fetch live weather if key provided
    if openweather_api_key and not pd.isna(flight['latitude']) and not pd.isna(flight['longitude']):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={flight['latitude']}&lon={flight['longitude']}&appid={openweather_api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                wind_speed_kt = data['wind']['speed'] * 1.94384
            else:
                wind_speed_kt = 10  # Default fallback
        except:
            wind_speed_kt = 10
    else:
        wind_speed_kt = 10

    features['wind_speed_kt'] = wind_speed_kt
    return features
