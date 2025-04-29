import os
import pandas as pd
import joblib

# Load model relative to repo structure
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', '..', 'models', 'fuel_burn_predictor.pkl')
model_path = os.path.abspath(model_path)

model = joblib.load(model_path)

# 🛠 Correct live prediction function
def predict_fuel_burn(distance_km, weather_penalty_factor=0.02, wind_speed_kt=10, deviation_flag=0, distance_penalty_km=0):
    """
    Predicts fuel burn for a live flight based on available features.
    Fallbacks to safe dummy values if some features missing.
    """

    # ✈️ Cruise speed assumption
    CRUISE_SPEED_KM_PER_HOUR = 850
    expected_flight_duration_sec = (distance_km / CRUISE_SPEED_KM_PER_HOUR) * 3600

    # 📋 Create full feature set
    X = pd.DataFrame({
        'distance_km': [distance_km],
        'weather_penalty_factor': [weather_penalty_factor],
        'deviation_flag': [deviation_flag],
        'wind_speed_kt': [wind_speed_kt],
        'expected_flight_duration_sec': [expected_flight_duration_sec],
        'distance_penalty_km': [distance_penalty_km]
    })

    pred = model.predict(X)
    return pred[0]
