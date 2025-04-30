def prepare_live_features(latitude, longitude, velocity, weather):
    """
    Prepare all required live features for fuel prediction.
    """
    base_distance_km = 3000
    cruise_speed_kts = 480
    wind_speed_kt = weather.get('wind_speed', 10) if weather else 10

    weather_penalty_factor = 0.0
    if wind_speed_kt > 20:
        weather_penalty_factor += 0.05
    if weather and weather.get('pressure', 1013) < 1000:
        weather_penalty_factor += 0.03

    features = {
        "distance_km": base_distance_km,
        "weather_penalty_factor": weather_penalty_factor,
        "deviation_flag": 0,
        "wind_speed_kt": wind_speed_kt,
        "expected_flight_duration_sec": int((base_distance_km / (cruise_speed_kts * 1.852)) * 3600),
        "distance_penalty_km": 0
    }
    return features
