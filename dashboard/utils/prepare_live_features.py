import pandas as pd

def prepare_live_features(flight_row, weather_info):
    features = {
        'distance_km': 3000,  # Assume dummy distance or compute based on lat/lon
        'weather_penalty_factor': 0.02,  # Assume dummy penalty
        'deviation_flag': 0,  # No deviation assumed live
        'wind_speed_kt': weather_info.get('wind_speed_kt', 10),
        'expected_flight_duration_sec': 3000 * (3600 / 850),  # Dummy speed 850 km/h
        'distance_penalty_km': 0  # Assume no holding
    }
    return pd.DataFrame([features])
