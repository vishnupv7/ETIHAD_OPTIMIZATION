
from utils.prepare_live_features import prepare_live_features
st.sidebar.subheader("📡 Live Data Debugging")
# ❌ No flights fetched
if flights_df.empty:
for idx, flight in flights_df.iterrows():

    weather = fetch_weather(lat, lon)

        
        col1.metric("Predicted Fuel Burn (kg)", f"{predicted_burn:.2f}")
            st.error("⚠️ High Wind Detected — Potential Fuel Risk!")
# 🔁 Auto-refresh
st.caption(f"🔁 Auto-refresh every {REFRESH_INTERVAL} seconds...")
time.sleep(REFRESH_INTERVAL)
