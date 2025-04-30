# 📦 model_predictor.py
import joblib
import pandas as pd

# ✅ Load trained model
model_path = "models/fuel_burn_predictor.pkl"
model = joblib.load(model_path)

# ✅ Safe prediction with correct feature names
def predict_fuel_burn_single(
    distance_km,
    weather_penalty_factor,
    deviation_flag,
    wind_speed_kt,
    expected_flight_duration_sec,
    distance_penalty_km
):
    # Create a DataFrame with expected schema
    X = pd.DataFrame([{
        "distance_km": distance_km,
        "weather_penalty_factor": weather_penalty_factor,
        "deviation_flag": deviation_flag,
        "wind_speed_kt": wind_speed_kt,
        "expected_flight_duration_sec": expected_flight_duration_sec,
        "distance_penalty_km": distance_penalty_km
    }])

    # ⚠️ Make prediction
    pred = model.predict(X)
    return pred[0]  # Return as float
