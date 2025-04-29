
import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🔺 Route View")

fig = px.scatter(df, x='distance_km', y='fuel_burn_kg', color='deviation_type',
                 title="Fuel Burn vs Distance by Route")

st.plotly_chart(fig)
