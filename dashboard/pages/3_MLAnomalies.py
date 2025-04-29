import streamlit as st
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🧠 ML Anomalies Detection")

anomalies = df[df['anomaly_score'] > 0.05]
st.metric("Anomaly Flights Detected", len(anomalies))

if anomalies.empty:
    st.success("🎉 No critical anomalies detected.")
else:
    st.warning("⚠️ Flights with unexpected CO₂ or Fuel Burn")
    st.dataframe(anomalies[['callsign', 'anomaly_score', 'shap_top_feature', 'weather_adjusted_fuel_burn_kg', 'predicted_fuel_burn_kg']])
