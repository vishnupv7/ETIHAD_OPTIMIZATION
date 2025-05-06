import streamlit as st
import pandas as pd
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn_single
from utils.prepare_live_features import prepare_live_features

# ✅ Safe default setup
if "data_mode" not in st.session_state:
    st.session_state["data_mode"] = "Live"

st.set_page_config(page_title="Live Monitoring - Etihad CO₂ Dashboard", layout="wide")
st.title("🛫 Live Monitoring - Etihad Airways Flights")

# ✅ Refresh button
if st.button("🔄 Refresh Now"):
    st.experimental_rerun()

OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

# ✅ Load Live Flights
st.subheader("🔎 Fetching Live OpenSky flights...")
live_flights = fetch_live_flights()

if live_flights.empty:
    st.warning("⚠️ No live Etihad flights detected currently.")
    st.stop()

# ✅ Filter ETD callsigns only
live_etihad_flights = live_flights[live_flights['callsign'].astype(str).str.startswith("ETD")]

if live_etihad_flights.empty:
    st.warning("⚠️ No ETD flights currently tracked.")
    st.stop()

st.success(f"✅ Live Etihad flights found: {len(live_etihad_flights)}")

for idx, flight in live_etihad_flights.iterrows():
    try:
        callsign = flight["callsign"].strip()
        lat = flight["latitude"]
        lon = flight["longitude"]
        vel = flight["velocity"]

        if pd.isna(lat) or pd.isna(lon):
            continue

        weather = fetch_weather(lat, lon, OPENWEATHER_API_KEY)

        features = prepare_live_features(latitude=lat, longitude=lon, velocity=vel, weather=weather)
        predicted_burn = predict_fuel_burn_single(**features)
        co2_emissions = predicted_burn * 3.16

        st.markdown("""
        ---
        """)
        st.subheader(f"✈️ Flight: {callsign}")
        st.metric("🛢️ Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
        st.metric("🌎 CO₂ Emissions (kg)", f"{co2_emissions:.2f}")
        st.metric("🌬️ Wind Speed (kt)", f"{features['wind_speed_kt']:.2f}")

    except Exception as e:
        st.error(f"❌ Prediction error for {flight['callsign']}: {e}")
