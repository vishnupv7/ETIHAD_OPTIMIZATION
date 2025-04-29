
import streamlit as st
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🌱 ESG Compliance Dashboard")

st.metric("Avg ESG Match %", f"{df['esg_match_percent'].mean():.1f}%")

st.bar_chart(df['esg_match_percent'])
