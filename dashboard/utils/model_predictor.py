import os
import pandas as pd
import joblib

# Correct way to build relative model path:
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', '..', 'models', 'fuel_burn_predictor.pkl')
model_path = os.path.abspath(model_path)

# ✅ Now load the model
model = joblib.load(model_path)

# Prediction function
def predict_fuel_burn(distance_km, weather_penalty_factor=0.02):
    X = pd.DataFrame({
        'distance_km': [distance_km],
        'weather_penalty_factor': [weather_penalty_factor]
    })
    pred = model.predict(X)
    return pred[0]
