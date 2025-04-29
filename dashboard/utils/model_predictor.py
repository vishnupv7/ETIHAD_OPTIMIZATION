# 📦 utils/model_predictor.py
import joblib
import pandas as pd
import os

# 📍 Load model once globally
model_path = '/content/ETIHAD_OPTIMIZATION/models/fuel_burn_predictor.pkl'

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model not found at: {model_path}")

model = joblib.load(model_path)

def predict_fuel_burn_single(features: dict):
    """
    Predict fuel burn for a single flight sample.

    Expected features:
    - distance_km
    - weather_penalty_factor
    - deviation_flag
    - wind_speed_kt
    - expected_flight_duration_sec
    - distance_penalty_km
    """
    required_features = [
        "distance_km",
        "weather_penalty_factor",
        "deviation_flag",
        "wind_speed_kt",
        "expected_flight_duration_sec",
        "distance_penalty_km"
    ]

    # Check missing fields
    missing = [f for f in required_features if f not in features]
    if missing:
        raise ValueError(f"Missing input fields: {missing}")

    # Prepare the feature dataframe
    X = pd.DataFrame([{k: features[k] for k in required_features}])

    # Predict fuel burn
    pred = model.predict(X)
    return pred[0]  # Return single prediction
