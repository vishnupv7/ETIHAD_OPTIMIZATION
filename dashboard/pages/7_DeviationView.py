
import streamlit as st
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🔄 Deviation View")

deviations = df[df['deviation_flag'] == 1]

st.dataframe(deviations[['callsign', 'deviation_type', 'distance_penalty_km']])
