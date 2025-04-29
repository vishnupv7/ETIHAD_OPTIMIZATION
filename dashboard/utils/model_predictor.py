import joblib
import pandas as pd
import os

# Load saved ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/fuel_burn_predictor.pkl')
model = joblib.load(MODEL_PATH)

# Required features for prediction
MODEL_FEATURES = ['distance_km', 'weather_penalty_factor']

def predict_fuel_burn(features_dict):
    filtered = {k: v for k, v in features_dict.items() if k in MODEL_FEATURES}
    X = pd.DataFrame([filtered])
    return model.predict(X)[0]
