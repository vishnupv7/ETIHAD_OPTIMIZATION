
# ✈️ Sample static flight to replay when no live data is found
def get_sample_flight():
    return {
        'callsign': 'ETD101',
        'distance_km': 11477,
        'wind_speed_kt': 12.0,
        'weather_penalty_factor': 0.02,
        'deviation_flag': 0,
        'expected_flight_duration_sec': 45000,
        'distance_penalty_km': 0
    }
