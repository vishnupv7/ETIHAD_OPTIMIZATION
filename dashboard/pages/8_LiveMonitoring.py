# 📄 dashboard/pages/8_LiveMonitoring.py (UPDATED FULLY)

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn_single
from utils.prepare_live_features import prepare_live_features

# ✅ Set page config immediately
st.set_page_config(page_title="Live Monitoring - Etihad CO2", layout="wide")

st.title("🛫 Live Flight Monitoring - Etihad Airways")
st.caption("Monitoring real-time flights, emissions, and weather impact.")

# ✅ Manual Refresh Button
refresh = st.button("🔁 Refresh Now")

if refresh:
    st.experimental_rerun()

# ✅ OpenWeather API Key (hidden or environment loaded in real app)
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

# ✅ Fetch Live Flights
flights_df = fetch_live_flights()

if flights_df.empty:
    st.warning("⚠️ No live Etihad flights detected from OpenSky public API.")
else:
    st.success(f"✅ Live Etihad flights found: {len(flights_df)}")

    for idx, row in flights_df.iterrows():
        try:
            callsign = row.get("callsign", "Unknown").strip()
            lat = row.get("latitude")
            lon = row.get("longitude")
            velocity = row.get("velocity")

            if pd.isna(lat) or pd.isna(lon):
                continue  # skip incomplete records

            # Fetch weather
            weather = fetch_weather(lat, lon, api_key=OPENWEATHER_API_KEY)

            wind_speed_kt = weather.get("wind_speed", 10) if weather else 10

            # Build the sample
            sample = {
                "callsign": callsign,
                "latitude": lat,
                "longitude": lon,
                "velocity": velocity,
                "wind_speed_kt": wind_speed_kt,
                "distance_km": 3000  # temporary placeholder assumed distance
            }

            # ✅ Filter fields
            filtered_sample = {
                "distance_km": sample.get("distance_km", 3000),
                "wind_speed_kt": sample.get("wind_speed_kt", 10)
            }

            # ✅ Prepare features safely
            prepared = prepare_live_features(**filtered_sample)

            # ✅ Predict
            pred_burn = predict_fuel_burn_single(**prepared)
            pred_co2 = pred_burn * 3.16  # ICAO multiplier

            # ✅ Display
            with st.expander(f"✈️ {callsign}", expanded=False):
                st.metric("Predicted Fuel Burn (kg)", f"{pred_burn:.2f}")
                st.metric("Predicted CO₂ Emissions (kg)", f"{pred_co2:.2f}")
                st.metric("Wind Speed (kt)", f"{wind_speed_kt:.2f}")

        except Exception as e:
            st.error(f"❌ Prediction error for {row.get('callsign', 'Unknown')}: {e}")

# ✅ Footer
st.caption("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
