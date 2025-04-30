# 📄 8_LiveMonitoring.py — Etihad Live Monitoring Page

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn_single
from utils.prepare_live_features import prepare_live_features

# ✅ Set Streamlit config
st.set_page_config(page_title="Live Monitoring - Etihad CO₂ Dashboard", layout="wide")

# 🔄 Manual refresh button
if st.button("🔄 Refresh Now"):
    st.rerun()

st.title("🛫 Live Monitoring - Etihad Airways Flights")
st.markdown("This page shows **live fuel predictions** for Etihad flights using OpenSky and OpenWeather.")

# ✅ Load OpenWeather API key
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

# ✅ Fetch real-time flight data
st.subheader("📡 Fetching live flights from OpenSky API...")
live_df = fetch_live_flights()

if live_df.empty:
    st.warning("⚠️ No live Etihad flights detected currently.")
    st.stop()

# ✅ Filter ETD flights only
etihad_flights = live_df[live_df['callsign'].astype(str).str.startswith('ETD')].copy()
st.success(f"✅ Live Etihad flights found: {len(etihad_flights)}")

# 🚀 Process each flight and predict fuel
for idx, row in etihad_flights.iterrows():
    try:
        callsign = str(row['callsign']).strip()
        lat = row.get('latitude')
        lon = row.get('longitude')
        velocity = row.get('velocity', 250)  # fallback cruise speed

        # 🌦️ Get weather
        weather = fetch_weather(lat, lon, api_key=OPENWEATHER_API_KEY)

        # 🧠 Prepare model features
        features = prepare_live_features(
            latitude=lat,
            longitude=lon,
            velocity=velocity,
            weather=weather
        )

        # 🎯 Predict fuel burn (kg)
        pred_burn = predict_fuel_burn_single(features)
        pred_co2 = pred_burn * 3.16

        # 📊 Display flight card
        with st.expander(f"✈️ {callsign} — Prediction Summary"):
            st.metric("Fuel Burn (kg)", f"{pred_burn:,.2f}")
            st.metric("CO₂ Emissions (kg)", f"{pred_co2:,.2f}")
            st.metric("Wind Speed", f"{features['wind_speed_kt']} kt")
            st.metric("Weather Penalty", f"{features['weather_penalty_factor']*100:.1f}%")

            if features["weather_penalty_factor"] > 0.05:
                st.warning("⚠️ Adverse weather conditions — potential fuel impact.")
            if features["distance_penalty_km"] > 50:
                st.warning("🔁 Possible route deviation detected.")

    except Exception as e:
        st.error(f"❌ Prediction error for {row.get('callsign')}: {e}")
