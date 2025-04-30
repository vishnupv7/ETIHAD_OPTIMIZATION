# 📦 model_predictor.py
import joblib
import pandas as pd

# ✅ Load trained model
model_path = "models/fuel_burn_predictor.pkl"
model = joblib.load(model_path)

# ✅ Safe prediction with exact schema
REQUIRED_FEATURES = [
    "distance_km",
    "weather_penalty_factor",
    "deviation_flag",
    "wind_speed_kt",
    "expected_flight_duration_sec",
    "distance_penalty_km"
]

def predict_fuel_burn_single(**features_dict):
    # Ensure all required features are present
    missing = [f for f in REQUIRED_FEATURES if f not in features_dict]
    if missing:
        raise ValueError(f"Missing features: {missing}")

    df = pd.DataFrame([features_dict])[REQUIRED_FEATURES]
    return model.predict(df)[0]
