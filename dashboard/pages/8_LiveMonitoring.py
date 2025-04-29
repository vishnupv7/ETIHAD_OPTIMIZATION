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
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"  # Your working key

# ✅ Refresh button
if st.button("🔄 Refresh Now"):
    st.experimental_rerun()

# ✅ Load Live Flights
st.subheader("🔎 Fetching Live OpenSky flights...")
live_flights = fetch_live_flights()

if live_flights.empty:
    st.warning("⚠️ No live Etihad flights detected currently.")
    st.stop()

# ✅ Filter ETD callsigns only
live_etihad_flights = live_flights[live_flights['callsign'].str.startswith('ETD', na=False)]

st.success(f"✅ Live Etihad flights found: {len(live_etihad_flights)}")

# ✅ Display flights
for idx, flight in live_etihad_flights.iterrows():
    try:
        callsign = str(flight['callsign']).strip()
        latitude = flight['latitude']
        longitude = flight['longitude']
        velocity = flight['velocity']

        # Skip if lat/lon missing
        if pd.isna(latitude) or pd.isna(longitude):
            continue

        # 🌦️ Fetch weather
        weather = fetch_weather(latitude, longitude, api_key=OPENWEATHER_API_KEY)

        # 🧠 Prepare model features
        sample = prepare_live_features(
            callsign=callsign,
            latitude=latitude,
            longitude=longitude,
            velocity=velocity,
            weather=weather,
        )

        # 🔥 Predict fuel burn
        pred_burn = predict_fuel_burn_single(**sample)

        # 🧮 Calculate CO₂ emissions
        pred_co2 = pred_burn * 3.16  # ICAO standard

        # 📋 Display info
        st.markdown("---")
        st.subheader(f"✈️ Flight: `{callsign}`")
        st.metric("🛢️ Predicted Fuel Burn (kg)", f"{pred_burn:.2f}")
        st.metric("🌎 Predicted CO₂ Emissions (kg)", f"{pred_co2:.2f}")
        st.metric("🌬️ Wind Speed (kt)", f"{sample['wind_speed_kt']:.1f}")
        
        # ⚡ Insights
        if sample['wind_speed_kt'] > 20:
            st.warning("⚡ Strong winds — consider adjusting cruise altitude!")

        if pred_co2 > 50000:
            st.error("🚨 High Emissions Flight Detected!")

    except Exception as e:
        st.error(f"❌ Prediction error for {flight['callsign']}: {e}")

# ⏳ Footer
st.caption("🔄 Dashboard refreshes manually when clicked. Live tracking powered by OpenSky & OpenWeather APIs.")
