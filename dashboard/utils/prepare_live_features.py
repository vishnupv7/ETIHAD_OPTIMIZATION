# utils/prepare_live_features.py

def prepare_live_features(distance_km, wind_speed_kt=10.0):
    """
    Prepare the live feature input exactly matching model expectations.
    - distance_km: required
    - wind_speed_kt: optional, default 10 kt
    """

    # Basic weather penalty factor (assumed logic)
    weather_penalty_factor = 0.02 if wind_speed_kt > 20 else 0.01

    return {
        "distance_km": distance_km,
        "weather_penalty_factor": weather_penalty_factor
    }
