# ✅ model_predictor.py — Live Prediction Engine
import joblib
import pandas as pd
import os

# 📍 Path to saved model
MODEL_PATH = os.path.join("models", "fuel_burn_predictor.pkl")

# ✅ Load trained model
model = joblib.load(MODEL_PATH)

def predict_fuel_burn_single(feature_dict):
    """
    Predict fuel burn using a complete feature dictionary.
    
    Expected Keys:
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
    
    # 🔍 Filter only required features
    filtered = {k: feature_dict.get(k, 0) for k in required_features}
    
    # 🔢 Convert to DataFrame for sklearn model
    df = pd.DataFrame([filtered])
    
    # 🎯 Predict fuel burn
    prediction = model.predict(df)
    
    return prediction[0]  # Return float (kg)
