
import streamlit as st
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.prepare_live_features import prepare_live_features
from utils.replay_sample import get_sample_flight
import pandas as pd

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Real Data or Replay)")

mode = st.radio("📡 Select Data Mode", ["Live", "Replay"], index=0)

if mode == "Live":
    flights_df = fetch_live_flights()
    if flights_df.empty:
        st.warning("😞 No Live Etihad Flights Detected")
        st.caption("Please check again later. No aircraft broadcasting under 'ETD%' at this moment.")
    else:
        for idx, flight in flights_df.iterrows():
            if pd.isna(flight['latitude']) or pd.isna(flight['longitude']):
                continue
            features = prepare_live_features(flight)
            if features is None:
                continue
            pred_burn = predict_fuel_burn(**features)

            st.subheader(f"✈️ {flight['callsign'].strip()} at {round(flight['latitude'],2)}, {round(flight['longitude'],2)}")
            st.metric("Predicted Fuel Burn (kg)", f"{pred_burn:.1f}")
            st.metric("Wind Speed", f"{features['wind_speed_kt']} kt")

            if features['wind_speed_kt'] > 15:
                st.warning("⚠️ High Wind Speed — Potential Fuel Penalty")
            if pred_burn > 25000:
                st.error("🔥 High Predicted Fuel Burn")

else:
    sample = get_sample_flight()
    pred_burn = predict_fuel_burn(**sample)
    st.subheader("🔁 Replay Mode: EY101 (AUH ➝ JFK)")
    st.metric("Predicted Fuel Burn", f"{pred_burn:.1f} kg")
    st.metric("Distance", f"{sample['distance_km']} km")
    st.metric("Wind Speed", f"{sample['wind_speed_kt']} kt")
    st.info("Insights based on real past flight — useful for demo/testing.")

st.caption("Module refreshes every 60 seconds on live mode.")


# 🔁 Auto-refresh Block (Debug)

from datetime import datetime

if mode == 'Live':
    st.caption(f"⏳ Auto-refreshing every 60 seconds... (Last updated: {datetime.now().strftime('%H:%M:%S')})")
    time.sleep(60)
    st.toast("Auto-refreshing now...")
    st.experimental_rerun()
