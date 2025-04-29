
# 📦 utils/prepare_live_features.py
import pandas as pd

def prepare_live_features(flight_row, weather_row):
    distance_km = 3000
    wind_speed_kt = weather_row.get('wind_speed', 0) * 1.94384
    wind_speed_kt = round(wind_speed_kt, 2)

    weather_penalty_factor = 0.02
    if wind_speed_kt > 15:
        weather_penalty_factor = 0.05
    elif wind_speed_kt > 10:
        weather_penalty_factor = 0.03

    deviation_flag = 0
    distance_penalty_km = 0
    CRUISE_SPEED_KMPH = 850
    expected_flight_duration_sec = (distance_km / CRUISE_SPEED_KMPH) * 3600

    features = pd.DataFrame({
        'distance_km': [distance_km],
        'weather_penalty_factor': [weather_penalty_factor],
        'deviation_flag': [deviation_flag],
        'wind_speed_kt': [wind_speed_kt],
        'expected_flight_duration_sec': [expected_flight_duration_sec],
        'distance_penalty_km': [distance_penalty_km]
    })
    return features
