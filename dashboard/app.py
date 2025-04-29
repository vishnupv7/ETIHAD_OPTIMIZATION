import streamlit as st
from utils.load_data import load_dashboard_data

st.set_page_config(page_title="Etihad CO2 Optimization Dashboard", layout="wide")
st.title("✈️ Etihad Airways - CO2 Optimization Dashboard")
st.write("Welcome to the enhanced real-time Fuel Efficiency, CO₂ Prediction, and ESG Alignment system.")
st.success("Use the sidebar to explore insights, predictions, and real-time flight analytics.")

# ---------------------------------------------
