import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🛰️ Flight Explorer")

fig = px.scatter(df, x='distance_km', y='weather_penalty_index',
                 color='deviation_type',
                 hover_name='callsign',
                 title="Flight Distance vs Weather Penalty Impact")

st.plotly_chart(fig)
