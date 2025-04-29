# 📄 dashboard/pages/8_LiveMonitoring.py

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from utils.model_predictor import predict_fuel_burn_single
from utils.fetch_live_data import fetch_live_flights, fetch_weather
from utils.prepare_live_features import prepare_live_features

# ✅ Page Setup FIRST (always first Streamlit call)
st.set_page_config(page_title="🛫 Live Monitoring - Etihad CO2 Optimization", layout="wide")

st.title("🛫 Live Flight Monitoring & Prediction - Etihad Airways")

# ✅ Sidebar Controls
mode = st.sidebar.radio("Select Mode:", ["Live API", "Replay Mode (Offline Data)"])
refresh_button = st.sidebar.button("🔄 Manual Refresh Now")
st.sidebar.caption("Data auto-refreshes every 2 minutes if in Live Mode.")

# ✅ Auto/manual refresh logic
if refresh_button:
    st.rerun()


# ✅ OpenWeather API Key
OPENWEATHER_API_KEY = "b20a349c98dba96ab2cb98e5fcf6891a"

# ✅ Main Logic
if mode == "Replay Mode (Offline Data)":
    st.warning("🕑 Replay mode active — historical flights dataset loaded.")

    try:
        df = pd.read_csv("data/processed/sample_replay_data.csv")
        st.success(f"✅ Loaded {len(df)} historical flights from Replay Mode!")
    except FileNotFoundError:
        st.error("❌ Replay dataset not found! Please upload or generate.")
        st.stop()

else:
    st.info("🛰️ Fetching Live OpenSky flights...")
    df_live = fetch_live_flights()

    if df_live.empty:
        st.warning("⚠️ No live Etihad flights currently airborne or visible on OpenSky.")
        st.stop()
    else:
        st.success(f"✅ Live Etihad flights found: {len(df_live)}")
        df = df_live

# ✅ Prepare data for prediction
prepared_data = []

for idx, row in df.iterrows():
    try:
        flight_features = prepare_live_features(row, openweather_api_key=OPENWEATHER_API_KEY)
        predicted_fuel = predict_fuel_burn_single(flight_features)

        prepared_data.append({
            "callsign": row['callsign'],
            "predicted_fuel_burn_kg": predicted_fuel,
            "predicted_co2_kg": predicted_fuel * 3.16,
            "wind_speed_kt": flight_features.get("wind_speed_kt", 0)
        })

    except Exception as e:
        st.error(f"❌ Prediction error for {row.get('callsign', 'Unknown')}: {e}")

# ✅ Convert results to DataFrame
pred_df = pd.DataFrame(prepared_data)

if not pred_df.empty:
    st.subheader("✈️ Live Predictions")
    st.dataframe(pred_df)

    # 📍 Optional: Plot flights if lat/lon exist
    if "latitude" in df.columns and "longitude" in df.columns:
        try:
            st.subheader("🌍 Live Flight Map (Etihad flights)")

            st.map(df[['latitude', 'longitude']].dropna())
        except:
            st.info("ℹ️ Mapping skipped — missing or invalid coordinates.")
else:
    st.warning("⚠️ No flights available for prediction.")

# 📅 Footer
st.caption(f"⏰ Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

# ✅ Optional: Manual Refresh Countdown
st.empty()  # Placeholder for future refresh timer

