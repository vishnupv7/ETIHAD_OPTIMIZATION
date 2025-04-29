import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🔍 Home - ESG Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Flights", len(df))
col2.metric("Total CO₂ (tons)", f"{df['weather_adjusted_co2_emissions_kg'].sum() / 1000:.2f}")
col3.metric("Avg ESG Match %", f"{df['esg_match_percent'].mean():.1f}%")
col4.metric("Total ASK (Million km)", f"{df['ASK'].sum()/1e6:.2f}")

st.subheader("⚠️ Alerts Summary")
alert_count = df[(df['anomaly_score'] > 0.05) | (df['deviation_flag'] == 1)].shape[0]
st.error(f"{alert_count} flights have significant anomalies or deviations.")

st.subheader("🧭 ESG Distribution")
fig = px.histogram(df, x='esg_match_percent', nbins=20, title="Distribution of ESG Compliance")
st.plotly_chart(fig)
