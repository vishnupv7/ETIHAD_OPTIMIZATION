import streamlit as st
import pandas as pd
import time
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.model_predictor import predict_fuel_burn
<<<<<<< HEAD

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🛫 Live Monitoring - Etihad CO2 Insights (Real Data Only)")

# 🔄 Auto refresh timer
REFRESH_INTERVAL = 60

# 📥 Fetch live flights
flights_df = fetch_live_flights()

# 📡 Live Data Debug
=======
from utils.prepare_live_features import prepare_live_features

st.set_page_config(page_title="Live Monitoring", layout="wide")
st.title("🛫 Live Monitoring - Etihad CO₂ Insights (Real Data Only)")

REFRESH_INTERVAL = 60
flights_df = fetch_live_flights()

>>>>>>> 97ed52d (🚀 Added models folder and enhanced live dashboard integration)
st.sidebar.subheader("📡 Live Data Debugging")
st.sidebar.write(f"Flights fetched: {flights_df.shape[0]}")
if not flights_df.empty:
    st.sidebar.dataframe(flights_df[['callsign', 'latitude', 'longitude', 'velocity']].head(10))

<<<<<<< HEAD
# ❌ No flights fetched
if flights_df.empty:
    st.warning("⚠️ No live Etihad flights detected from OpenSky API right now.")
    st.stop()  # ❗ Stop the app if no real data

# 🚀 Show real flights
=======
if flights_df.empty:
    st.markdown("### 😞 No Live Etihad Flights Detected")
    st.markdown("Please check again later. No aircraft broadcasting under 'ETD%' at this moment.")
    st.image("https://cdn-icons-png.flaticon.com/512/408/408172.png", width=100)
    st.stop()

>>>>>>> 97ed52d (🚀 Added models folder and enhanced live dashboard integration)
for idx, flight in flights_df.iterrows():
    callsign = flight.get('callsign', 'Unknown')
    lat = flight.get('latitude', None)
    lon = flight.get('longitude', None)
<<<<<<< HEAD

    # 📡 Fetch Weather for the flight location
    weather = fetch_weather(lat, lon)
    if not weather:
        st.error(f"🌧️ Weather API fetch failed for {callsign}. Skipping.")
        continue  # Skip this flight if no weather info

    distance_km = 3000  # Placeholder because OpenSky doesn't provide direct distance
    predicted_burn = predict_fuel_burn(distance_km, weather_penalty_factor=0.02, wind_speed_kt=weather['wind_speed'])
=======
    weather = fetch_weather(lat, lon)

    if not weather:
        st.warning(f"🌧️ Weather fetch failed for {callsign}. Skipping.")
        continue

    features = prepare_live_features(flight, weather)
    predicted_burn = predict_fuel_burn(**features.iloc[0].to_dict())
>>>>>>> 97ed52d (🚀 Added models folder and enhanced live dashboard integration)

    with st.container():
        st.subheader(f"✈️ Flight: {callsign.strip()}")
        col1, col2, col3, col4 = st.columns(4)
<<<<<<< HEAD
        
        col1.metric("Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
        col2.metric("Wind Speed (kt)", f"{weather['wind_speed']:.2f}")
        col3.metric("Pressure (hPa)", f"{weather['pressure']}")
        col4.metric("Temperature (°C)", f"{weather['temperature']}")

        if weather['wind_speed'] > 15:
=======
        col1.metric("Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
        col2.metric("Wind Speed (kt)", f"{features['wind_speed_kt'].values[0]:.2f}")
        col3.metric("Pressure (hPa)", f"{weather['pressure']}")
        col4.metric("Temperature (°C)", f"{weather['temperature']}")

        if features['wind_speed_kt'].values[0] > 15:
>>>>>>> 97ed52d (🚀 Added models folder and enhanced live dashboard integration)
            st.error("⚠️ High Wind Detected — Potential Fuel Risk!")
        if predicted_burn > 25000:
            st.error("⚠️ High Predicted Fuel Burn!")
        if weather['pressure'] < 1000:
            st.warning("⛅ Low Pressure — Diversion Risk!")

<<<<<<< HEAD
# 🔁 Auto-refresh
st.caption(f"🔄 Auto-refreshing every {REFRESH_INTERVAL} seconds...")
=======
st.caption(f"🔁 Auto-refresh every {REFRESH_INTERVAL} seconds...")
>>>>>>> 97ed52d (🚀 Added models folder and enhanced live dashboard integration)
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
