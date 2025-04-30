# 📄 prepare_live_features.py
# ✅ Generates 6 features from OpenSky + OpenWeather input
# ✅ Matches model: distance_km, weather_penalty_factor, deviation_flag, wind_speed_kt, expected_flight_duration_sec, distance_penalty_km

def prepare_live_features(latitude, longitude, velocity, weather):
    """
    Prepare live features for prediction from OpenSky & OpenWeather data.
    Returns a dict with all 6 features required by the ML model.
    """

    # --- Assumptions ---
    base_distance_km = 3000  # Average long-haul Etihad route
    cruise_speed_kts = 480   # Cruise speed in knots

    # --- Convert weather to usable values ---
    wind_speed_kt = 0
    pressure = 1013  # default sea-level standard

    if weather:
        wind_speed_kt = weather.get("wind", {}).get("speed", 0) * 1.94384  # m/s to knots
        pressure = weather.get("main", {}).get("pressure", 1013)

    # --- Weather Penalty Factor ---
    weather_penalty_factor = 0.0
    if wind_speed_kt > 20:
        weather_penalty_factor += 0.05
    if pressure < 1000:
        weather_penalty_factor += 0.03

    # --- Deviation Proxy ---
    deviation_flag = 0  # No deviation logic yet, default 0
    distance_penalty_km = 0  # No penalty assumed in real-time mode

    # --- Estimated Flight Duration ---
    # Convert cruise speed (knots) to km/s: 1 knot = 1.852 km/h = 0.000514444 km/s
    cruise_speed_km_per_sec = cruise_speed_kts * 1.852 / 3600
    expected_flight_duration_sec = base_distance_km / cruise_speed_km_per_sec

    return {
        "distance_km": base_distance_km,
        "weather_penalty_factor": weather_penalty_factor,
        "deviation_flag": deviation_flag,
        "wind_speed_kt": wind_speed_kt,
        "expected_flight_duration_sec": expected_flight_duration_sec,
        "distance_penalty_km": distance_penalty_km
    }
