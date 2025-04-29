def prepare_live_features(row):
    return {
        'callsign': row.get('callsign', 'Unknown'),
        'distance_km': row.get('distance_km', 3000),
        'weather_penalty_factor': 0.02,  # Default fallback
        'wind_speed_kt': row.get('wind_speed_kt', 0),
        'expected_flight_duration_sec': row.get('expected_flight_duration_sec', 0),
        'deviation_flag': row.get('deviation_flag', 0),
        'distance_penalty_km': row.get('distance_penalty_km', 0)
