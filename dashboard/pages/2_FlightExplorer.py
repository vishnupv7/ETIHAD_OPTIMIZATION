
import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🛰️ Flight Explorer")

fig = px.scatter_geo(df, lat='departure_lat', lon='departure_lon', 
                     color='weather_penalty_index', size='distance_km',
                     hover_name='callsign', title="Flight Distance vs Weather Penalty")

st.plotly_chart(fig)
