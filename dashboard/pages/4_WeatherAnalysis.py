import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🌧️ Weather Impact Analysis")

fig = px.histogram(df, x='weather_penalty_index', nbins=20, title="Weather Penalty Index Distribution")
st.plotly_chart(fig)

st.subheader("🚨 Flights With High Weather Impact")
weather_affected = df[df['weather_penalty_index'] > 1]
st.dataframe(weather_affected[['callsign', 'weather_penalty_index', 'departure_weather']])
