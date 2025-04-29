import joblib
import pandas as pd

# Load saved ML model
model_path = '/content/drive/MyDrive/Etihad_Optimization/models/fuel_burn_predictor.pkl'
model = joblib.load(model_path)

# Predict fuel burn given distance_km and weather penalty
def predict_fuel_burn(distance_km, weather_penalty_factor=0.02):
    # Features to pass to model
    X = pd.DataFrame({
        'distance_km': [distance_km],
        'weather_penalty_factor': [weather_penalty_factor]
    })
    pred = model.predict(X)
    return pred[0]