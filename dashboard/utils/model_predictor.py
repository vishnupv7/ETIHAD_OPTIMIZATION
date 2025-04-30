# utils/model_predictor.py
import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("models", "fuel_burn_predictor.pkl")
model = joblib.load(MODEL_PATH)

def predict_fuel_burn_single(features: dict):
    X = np.array([[features[k] for k in [
        "distance_km",
        "weather_penalty_factor",
        "deviation_flag",
        "wind_speed_kt",
        "expected_flight_duration_sec",
        "distance_penalty_km"
    ]]])
    return model.predict(X)[0]
