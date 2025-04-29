
import streamlit as st
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🔎 Home - ESG Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Flights", len(df))
col2.metric("Total CO2 (tons)", f"{df['weather_adjusted_co2_emissions_kg'].sum()/1000:.2f}")
col3.metric("Avg ESG Match %", f"{df['esg_match_percent'].mean():.1f}%")
col4.metric("Total ASK (Million km)", f"{df['ASK'].sum()/1e6:.2f}")

st.subheader("Alerts")
alerts = df[(df['anomaly_score'] > 0.05) | (df['deviation_flag'] == 1)]
st.write(f"{len(alerts)} flights have significant anomalies or deviations.")
