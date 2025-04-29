# ✅ model_predictor.py (Final Corrected)
import joblib
import numpy as np

# Load trained model
model_path = "models/fuel_burn_predictor.pkl"
model = joblib.load(model_path)

# Single flight prediction function
def predict_fuel_burn_single(distance_km, wind_speed_kt):
    # Approximate weather penalty factor based on wind speed
    weather_penalty_factor = min(0.1, wind_speed_kt / 100)  # 10% max penalty
    X = np.array([[distance_km, weather_penalty_factor]])
    prediction = model.predict(X)
    return prediction[0]  # Return as single float
