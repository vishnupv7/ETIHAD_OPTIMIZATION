import streamlit as st
from utils.load_data import load_dashboard_data

df = load_dashboard_data()

st.title("🔄 Deviation View")

st.write("Flights tagged as rerouted, shortened, or holding.")
deviations = df[df['deviation_flag'] == 1]

if deviations.empty:
    st.success("✅ No significant deviations detected.")
else:
    st.warning(f"{len(deviations)} flights deviated from optimal route")
    st.dataframe(deviations[['callsign', 'deviation_type', 'distance_penalty_km', 'duration_deviation_ratio']])
