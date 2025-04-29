
import requests
import datetime

def test_opensky_connection(username, password):
    url = "https://opensky-network.org/api/states/all"
    try:
        r = requests.get(url, auth=(username, password), timeout=15)
        if r.status_code != 200:
            return f"❌ HTTP {r.status_code}: {r.text}"
        data = r.json()
        if not data.get("states"):
            return "⚠️ No flight data returned. Possibly no aircraft broadcasting currently."
        etd_flights = [s for s in data["states"] if s[1] and str(s[1]).strip().startswith("ETD")]
        if not etd_flights:
            return "⚠️ API working but no Etihad (ETD%) flights detected."
        return f"✅ API Live! Found {len(etd_flights)} ETD flights."
    except Exception as e:
        return f"🚨 API call failed: {e}"
