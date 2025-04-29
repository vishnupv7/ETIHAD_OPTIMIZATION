import streamlit as st
import plotly.express as px
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🌱 ESG Compliance Dashboard")

avg_esg = df['esg_match_percent'].mean()
st.metric("Avg ESG Match %", f"{avg_esg:.1f}%")

fig = px.box(df, y='esg_match_percent', title="ESG Compliance Score Spread")
st.plotly_chart(fig)
