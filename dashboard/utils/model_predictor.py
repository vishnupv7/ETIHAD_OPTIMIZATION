import joblib
import pandas as pd
import os

# ✅ Load model only once
MODEL_PATH = os.path.join('models', 'fuel_burn_predictor.pkl')

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Model load failed: {e}")

# ✅ Correct expected features
REQUIRED_FEATURES = [
    'distance_km',
    'weather_penalty_factor',
    'deviation_flag',
    'wind_speed_kt',
    'expected_flight_duration_sec',
    'distance_penalty_km'
]

def predict_fuel_burn_single(features: dict) -> float:
    """
    Predict fuel burn for a single flight given live features.
    """
    if model is None:
        raise ValueError("Fuel burn model is not loaded.")
    
    # Build input DataFrame with correct feature names
    try:
        input_df = pd.DataFrame([{feat: features.get(feat, 0) for feat in REQUIRED_FEATURES}])
    except Exception as e:
        raise ValueError(f"Error preparing input for prediction: {e}")

    # Predict
    prediction = model.predict(input_df)[0]
    return prediction
