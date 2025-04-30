# 📄 8_LiveMonitoring.py — Etihad Live Monitoring Page

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn_single
from utils.prepare_live_features import prepare_live_features

# ✅ Set page config at very beginning
st.set_page_config(page_title="Live Monitoring - Etihad CO₂ Dashboard", layout="wide")

# ✅ Page title
st.title("🛫 Live Monitoring - Etihad Airways Flights")

# ✅ OpenWeather API Key
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"  # Replace with secure method in prod

# ✅ Refresh button
if st.button("🔄 Refresh Now"):
    st.rerun()

# ✅ Load Live Flights
st.subheader("🔎 Fetching Live OpenSky flights...")
live_flights = fetch_live_flights()

if live_flights.empty:
    st.warning("⚠️ No live Etihad flights detected currently.")
    st.stop()

# ✅ Filter ETD callsigns only
live_etihad_flights = live_flights[live_flights['callsign'].astype(str).str.startswith("ETD")]

if live_etihad_flights.empty:
    st.info("ℹ️ No Etihad flights currently active in OpenSky stream.")
    st.stop()

# ✅ Iterate over each Etihad flight
for idx, row in live_etihad_flights.iterrows():
    callsign = row['callsign'].strip()
    lat = row['latitude']
    lon = row['longitude']
    vel = row['velocity']

    if pd.isna(lat) or pd.isna(lon):
        continue

    # Fetch weather
    weather = fetch_weather(lat, lon, OPENWEATHER_API_KEY)

    sample = {
        "callsign": callsign,
        "latitude": lat,
        "longitude": lon,
        "velocity": vel,
        "weather": weather
    }

    required_keys = {'latitude', 'longitude', 'velocity', 'weather'}
    if not required_keys.issubset(sample):
        st.warning(f"⚠️ Missing keys for prediction in {callsign}")
        continue

    try:
        # Extract only valid inputs
        clean_input = {
            "latitude": sample["latitude"],
            "longitude": sample["longitude"],
            "velocity": sample["velocity"],
            "weather": sample["weather"]
        }
        features = prepare_live_features(**clean_input)
        distance_km = features["distance_km"]
        wind_speed_kt = sample.get("weather", {}).get("wind", {}).get("speed", 5) * 1.94384
        predicted_burn = predict_fuel_burn_single(distance_km, wind_speed_kt)
        co2_emissions = predicted_burn * 3.16

        st.subheader(f"✈️ Flight: {callsign}")
        st.metric("🛢️ Predicted Fuel Burn (kg)", f"{predicted_burn:,.2f}")
        st.metric("🌍 CO₂ Emissions (kg)", f"{co2_emissions:,.2f}")
        st.metric("🌬️ Wind Speed (kt)", f"{wind_speed_kt:.1f}")

    except Exception as e:
        st.error(f"❌ Prediction error for {callsign}: {e}")
        continue
