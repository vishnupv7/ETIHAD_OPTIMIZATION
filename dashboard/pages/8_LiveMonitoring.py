import streamlit as st
import pandas as pd
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Live + Replay)")

# ✅ Manual Refresh Button
if st.button("🔁 Refresh Now"):
    st.experimental_rerun()

# ✅ Mode Selector
mode = st.radio("🛰️ Choose Mode", ["Live", "Replay (Sample Data)"], horizontal=True)

# ✅ Fetch or Prepare Flight Data
flights_df = fetch_live_flights()

if flights_df.empty and mode == "Live":
    st.warning("⚠️ No live Etihad flights detected.")
    st.stop()

if mode == "Replay (Sample Data)":
    sample_data = pd.DataFrame([{
        'callsign': 'ETD100',
        'distance_km': 11500,
        'wind_speed_kt': 12.0,
        'weather_penalty_factor': 0.02,
        'deviation_flag': 0,
        'expected_flight_duration_sec': 42000,
        'distance_penalty_km': 0,
        'pressure': 1008
    }])
    st.success("📦 Using Replay Sample Data")
    flights = sample_data
else:
    flights = prepare_live_features(flights_df)
    if flights.empty:
        st.warning("⚠️ No valid flights available after feature preparation.")
        st.stop()

# ✅ Flight-wise Prediction and Insights
for idx, row in flights.iterrows():
    callsign = row.get("callsign", f"Flight {idx}")

    try:
        pred_burn = predict_fuel_burn(
            distance_km=row.get("distance_km", 3000),
            weather_penalty_factor=row.get("weather_penalty_factor", 0.02),
            deviation_flag=row.get("deviation_flag", 0),
            wind_speed_kt=row.get("wind_speed_kt", 0),
            expected_flight_duration_sec=row.get("expected_flight_duration_sec", 0),
            distance_penalty_km=row.get("distance_penalty_km", 0)
        )

        with st.expander(f"✈️ {callsign} — Predicted Fuel Burn: {pred_burn:.2f} kg"):
            st.metric("Predicted Fuel Burn", f"{pred_burn:.2f} kg")
            st.metric("Wind Speed", f"{row.get('wind_speed_kt', 0)} kt")
            st.metric("Pressure", row.get("pressure", "N/A"))

            # 🔴 Alerts based on conditions
            if row.get("wind_speed_kt", 0) > 15:
                st.warning("💨 High Winds — Possible Increased Fuel Usage")
            if pred_burn > 25000:
                st.error("🔥 High Predicted Fuel Burn — Route Optimization Suggested")
            if row.get("pressure", 1013) < 1000:
                st.warning("🌫️ Low Pressure Detected — Potential Weather Impact")

    except Exception as e:
        st.error(f"❌ Prediction failed for {callsign}: {e}")

# ✅ Footer timestamp
st.caption(f"⏱ Last updated: {datetime.now().strftime('%H:%M:%S')} — Manual refresh above.")
