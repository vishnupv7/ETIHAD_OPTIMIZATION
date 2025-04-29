import joblib
import pandas as pd
import os

# 🛫 Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/fuel_burn_predictor.pkl')
model = joblib.load(MODEL_PATH)

def predict_fuel_burn_single(features: dict):
    # Expected features: distance_km, wind_speed_kt, deviation_flag, expected_flight_duration_sec, distance_penalty_km
    expected_cols = ['distance_km', 'wind_speed_kt', 'deviation_flag', 'expected_flight_duration_sec', 'distance_penalty_km']
    data = pd.DataFrame([features], columns=expected_cols)
    prediction = model.predict(data)[0]
    return predictio
