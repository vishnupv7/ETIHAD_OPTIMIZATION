from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.clean_live_flight_data import clean_live_flight_data
import streamlit as st
import pandas as pd
import time

st.title("🛫 Live Monitoring - Etihad CO2 Insights")

flights_df = fetch_live_flights()
flights_df = clean_live_flight_data(flights_df)

# 🔥 Check if no live flights fetched
if flights_df.empty:
    st.warning("⚠️ No live Etihad flights detected. Showing demo flights!")
    flights_df = pd.DataFrame({
        'callsign': ['ETD123', 'ETD456'],
        'latitude': [24.4539, 25.276987],
        'longitude': [54.3773, 55.296249],
        'velocity': [210, 230],
    })

# 🚀 Loop through flights
for idx, flight in flights_df.iterrows():
    callsign = flight['callsign']
    lat = flight['latitude']
    lon = flight['longitude']
    
    # Dummy weather if not available
    weather = fetch_weather(lat, lon) or {
        'wind_speed': 5,
        'wind_deg': 90,
        'pressure': 1015,
        'temperature': 30
    }
    
    distance_km = 3000  # Estimate
    predicted_burn = predict_fuel_burn(distance_km, weather_penalty_factor=0.02)
    
    st.subheader(f"✈️ Flight: {callsign}")
    st.metric("Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
    st.metric("Wind Speed (kt)", f"{weather['wind_speed']}")
    st.metric("Pressure (hPa)", f"{weather['pressure']}")
    
    if weather['wind_speed'] > 15:
        st.error("⚠️ High Winds Detected!")
    if predicted_burn > 25000:
        st.error("⚠️ High Fuel Burn Alert!")

# Auto-refresh
REFRESH_INTERVAL = 60
st.caption(f"Auto-refreshing every {REFRESH_INTERVAL} seconds...")
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
