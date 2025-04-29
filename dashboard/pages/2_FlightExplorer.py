import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🛰️ Flight Explorer")
st.write("Explore fuel performance and routing characteristics of each flight.")

filtered = df[df['deviation_type'].notna()]
fig = px.scatter(filtered, x='distance_km', y='weather_penalty_index',
                 color='deviation_type',
                 hover_data=['callsign', 'fuel_burn_kg'],
                 title="Flight Distance vs Weather Penalty Impact")
st.plotly_chart(fig)
