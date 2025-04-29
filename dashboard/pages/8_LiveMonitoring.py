import streamlit as st
import pandas as pd
import time
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Real Data Only)")

REFRESH_INTERVAL = 60

# Fetch live Etihad flights
flights_df = fetch_live_flights()

st.sidebar.subheader("📡 Live Data Debugging")
st.sidebar.write(f"Flights fetched: {flights_df.shape[0]}")
if not flights_df.empty:
    st.sidebar.dataframe(flights_df[['callsign', 'latitude', 'longitude', 'velocity']].head(10))

if flights_df.empty:
    st.markdown("### 😞 No Live Etihad Flights Detected")
    st.markdown("Please check again later. No aircraft broadcasting under 'ETD%' at this moment.")
    st.image("https://cdn-icons-png.flaticon.com/512/408/408172.png", width=100)
    st.stop()

# Loop through live flights
for idx, flight in flights_df.iterrows():
    callsign = flight.get('callsign', 'Unknown')
    lat = flight.get('latitude', None)
    lon = flight.get('longitude', None)

    if pd.isna(lat) or pd.isna(lon):
        continue

    weather = fetch_weather(lat, lon)
    if not weather:
        st.warning(f"🌧️ Weather fetch failed for {callsign}. Skipping.")
        continue

    features = prepare_live_features(flight, weather)
    predicted_burn = predict_fuel_burn(**features.iloc[0].to_dict())

    with st.container():
        st.subheader(f"✈️ Flight: {callsign.strip()}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
        col2.metric("Wind Speed (kt)", f"{features['wind_speed_kt'].values[0]:.2f}")
        col3.metric("Pressure (hPa)", f"{weather['pressure']}")
        col4.metric("Temperature (°C)", f"{weather['temperature']}")

        if features['wind_speed_kt'].values[0] > 15:
            st.error("⚠️ High Wind Detected — Potential Fuel Risk!")
        if predicted_burn > 25000:
            st.error("⚠️ High Predicted Fuel Burn!")
        if weather['pressure'] < 1000:
            st.warning("⛅ Low Pressure — Diversion Risk!")

st.caption(f"🔁 Auto-refreshing every {REFRESH_INTERVAL} seconds...")
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
