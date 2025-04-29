import streamlit as st
import pandas as pd
import time
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring - Etihad CO₂ Insights", layout="wide")

st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Real Data or Replay)")

# Mode Selector: Live or Replay
mode = st.radio("📌 Select Data Mode", ['Live', 'Replay'], horizontal=True)

# Load live flights
flights_df = fetch_live_flights()

if flights_df.empty:
    st.warning("😞 No Live Etihad Flights Detected")
    st.write("Please check again later. No aircraft broadcasting under 'ETD%' at this moment.")
    st.caption("Module refreshes every 60 seconds on live mode.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzgyNnhlOTB3d3ZndGR6Nms4ZDJ4aWlscGVkZW8xaGprMTJxdml6byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NG0k29AvIp7kfNQnw7/giphy.gif", width=200)
    st.stop()

# Prepare features
live_data = prepare_live_features(flights_df)

# Display Mode
if mode == 'Live':
    st.success(f"✅ {len(live_data)} Live Etihad Flights Fetched!")
    st.caption("Module refreshes every 60 seconds automatically.")
else:
    st.info(f"📂 Replay Mode: Simulated based on last fetched live data.")
    # Simulate replay mode by slicing 5 random rows
    live_data = live_data.sample(min(5, len(live_data)))

# Display table
st.dataframe(live_data[['callsign', 'latitude', 'longitude', 'wind_speed_kt']], use_container_width=True)

# Predict and Visualize
st.header("🔮 Real-Time Fuel Predictions & Alerts")

for idx, sample in live_data.iterrows():
    callsign = sample.get('callsign', 'Unknown')
    
    # Safely prepare inputs
    pred_burn = predict_fuel_burn(
        distance_km=sample.get('distance_km', 3000),
        weather_penalty_factor=sample.get('weather_penalty_factor', 0.02),
        deviation_flag=sample.get('deviation_flag', 0),
        wind_speed_kt=sample.get('wind_speed_kt', 0),
        expected_flight_duration_sec=sample.get('expected_flight_duration_sec', 0),
        distance_penalty_km=sample.get('distance_penalty_km', 0)
    )

    with st.expander(f"✈️ {callsign} — Predicted Fuel Burn: {pred_burn:.2f} kg"):
        st.metric("Predicted Fuel Burn (kg)", f"{pred_burn:.2f}")
        st.metric("Wind Speed (kt)", sample.get('wind_speed_kt', 0))
        st.metric("Pressure (hPa)", sample.get('pressure', 'N/A'))
        
        # 🚨 Alerts
        if sample.get('wind_speed_kt', 0) > 15:
            st.error("⚡ High Winds: May Cause Higher Fuel Consumption")
        if pred_burn > 25000:
            st.error("⚡ High Fuel Burn Predicted")
        if sample.get('pressure', 1013) < 1000:
            st.warning("🌫️ Possible Low Pressure Zone - Monitor Flight Altitude")

# Auto Refresh
if mode == 'Live':
    st.caption("⏳ Auto-refreshing every 60 seconds...")
    time.sleep(60)
    st.experimental_rerun()
