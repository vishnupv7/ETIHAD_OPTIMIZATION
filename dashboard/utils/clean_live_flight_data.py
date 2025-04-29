import pandas as pd
import numpy as np

def clean_live_flight_data(flights_df):
    """
    Takes raw filtered ETD live flight DataFrame, applies basic cleaning and standardization.
    """

    if flights_df.empty:
        return flights_df

    # 1️⃣ Remove entries without latitude or longitude
    flights_df = flights_df.dropna(subset=['latitude', 'longitude'])

    # 2️⃣ Clean callsign formatting
    flights_df['callsign'] = flights_df['callsign'].astype(str).str.strip()

    # 3️⃣ Create estimated departure time if missing
    flights_df['departure_time'] = flights_df['time_position'].fillna(flights_df['last_contact'])

    # 4️⃣ Default estimated arrival time (assume 6 hours ahead if unknown)
    flights_df['arrival_time'] = flights_df['last_contact'] + (6 * 3600)

    # 5️⃣ Assign dummy departure and arrival airports (to be improved later if needed)
    flights_df['estdepartureairport'] = 'OMAA'  # Abu Dhabi Hub
    flights_df['estarrivalairport'] = 'Unknown'

    # 6️⃣ Distance assumption (dummy ~ 3000 km if not computed)
    flights_df['distance_km'] = 3000

    # 7️⃣ Default weather penalty score if missing (2% assumption)
    flights_df['weather_penalty_score'] = 0.02

    # 8️⃣ Fill missing fields
    for field in ['velocity', 'baro_altitude', 'geo_altitude']:
        if field not in flights_df.columns:
            flights_df[field] = np.nan

    # 9️⃣ Create schema-compatible columns
    flights_df['fuel_burn_kg'] = np.nan
    flights_df['co2_emissions_kg'] = np.nan
    flights_df['fuel_burn_kg_adjusted'] = np.nan
    flights_df['co2_emissions_kg_adjusted'] = np.nan

    return flights_df