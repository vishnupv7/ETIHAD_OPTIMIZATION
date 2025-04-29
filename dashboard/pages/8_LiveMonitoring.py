import streamlit as st
import pandas as pd
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring - Etihad CO₂", layout="wide")

# --- UI Header ---
st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Live + Replay)")

# --- Manual Refresh Button ---
if st.button("🔁 Refresh Now"):
    st.session_state.manual_refresh = True
    st.success("🔄 Manual refresh triggered!")

# --- Data Mode Selection ---
mode = st.radio("🧭 Choose Mode", ['Live', 'Replay (Sample Data)'], horizontal=True)

# --- Load Data ---
if mode == 'Live':
    df = fetch_live_flights()
    st.caption("🛰 Live OpenSky flight data fetched")
else:
    df = pd.read_csv("data/processed/sample_replay_data.csv")
    st.info("📦 Using Replay Sample Data")

# --- Validate ---
if df.empty:
    st.warning("⚠️ No live Etihad flights detected.")
    st.caption("Please check again later. No aircraft broadcasting under 'ETD%' at this moment.")
else:
    for _, row in df.iterrows():
        try:
            # Prepare features
            sample = prepare_live_features(row)
            burn = predict_fuel_burn(sample)

            # Display
            st.subheader(f"✈️ Flight: {sample['callsign']}")
            st.metric("Predicted Fuel Burn (kg)", f"{burn:.2f}")
            st.metric("Wind Speed (kt)", f"{sample['wind_speed_kt']:.1f}")
            st.caption(f"Distance: {sample['distance_km']} km | Penalty: {sample['weather_penalty_factor']:.2f}")

            if sample['wind_speed_kt'] > 25:
                st.error("🌪 High Wind Risk — Optimize Altitude")
            if burn > 25000:
                st.warning("🛢 High Predicted Fuel Burn")

        except Exception as e:
            st.error(f"❌ Prediction failed for {row.get('callsign', 'N/A')}: {e}")

# --- Footer ---
st.caption(f"🕒 Last checked: {datetime.now().strftime('%H:%M:%S')} — Click [🔁 Refresh Now] to re-fetch")
