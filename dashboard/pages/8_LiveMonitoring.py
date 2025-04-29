import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn_single
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring - Etihad CO₂", layout="wide")

st.title("🛫 Live Monitoring - Etihad Real-Time CO₂ Insights")

# ✅ Auto/manual refresh
refresh_button = st.button("🔄 Refresh Live Data")

# ✅ OpenWeather API Key
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

# ✅ Fetch live flights
st.subheader("🔎 Fetching Live OpenSky flights...")
flights_df = fetch_live_flights()

if flights_df.empty:
    st.error("⚠️ No live Etihad flights detected right now. Waiting for data...")
else:
    st.success(f"✅ Live Etihad flights found: {len(flights_df)}")

    for idx, flight in flights_df.iterrows():
        try:
            lat = flight['latitude']
            lon = flight['longitude']
            callsign = str(flight['callsign']).strip()

            if pd.isna(lat) or pd.isna(lon) or not callsign:
                continue

            # 🌦️ Fetch weather
            weather = fetch_weather(lat, lon, api_key=OPENWEATHER_API_KEY)
            wind_speed_kt = weather.get('wind_speed', 10)

            # 📈 Prepare feature input
            sample_features = prepare_live_features(
                distance_km=3000,  # Assumed standard cruise distance
                wind_speed_kt=wind_speed_kt,
                deviation_flag=0,
                expected_flight_duration_sec=12600,
                distance_penalty_km=0
            )

            # 🔥 Predict
            pred_burn = predict_fuel_burn_single(sample_features)
            pred_co2 = pred_burn * 3.16

            st.markdown(f"""
            ---
            ✈️ **Flight:** `{callsign}`  
            🛢️ **Predicted Fuel Burn:** `{pred_burn:.2f} kg`  
            🌎 **Predicted CO₂ Emissions:** `{pred_co2:.2f} kg`  
            🌬️ **Wind Speed:** `{wind_speed_kt:.1f} kt`
            ---
            """)
        except Exception as e:
            st.error(f"❌ Prediction error for {callsign}: {e}")

st.caption("🕒 This page shows real-time OpenSky flights + live weather impact.")
