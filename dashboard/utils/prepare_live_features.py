def prepare_live_features(
    callsign,
    latitude,
    longitude,
    velocity,
    distance_km=3000,
    wind_speed_kt=10,
    pressure=1013,
    expected_flight_duration_sec=14400,
    deviation_flag=0
):
    return {
        "callsign": callsign,
        "latitude": latitude,
        "longitude": longitude,
        "velocity": velocity,
        "distance_km": distance_km,
        "wind_speed_kt": wind_speed_kt,
        "pressure": pressure,
        "expected_flight_duration_sec": expected_flight_duration_sec,
        "deviation_flag": deviation_flag,
    }
