# 📂 Corrected load_data.py (works both locally and on Streamlit Cloud)

import pandas as pd
import os

def load_dashboard_data():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Move up one level to dashboard/
    dashboard_dir = os.path.dirname(current_dir)
    
    # Path to data/processed/final_dashboard_dataset.csv relative to dashboard/
    data_path = os.path.join(dashboard_dir, '..', 'data', 'processed', 'final_dashboard_dataset.csv')
    data_path = os.path.normpath(data_path)  # Clean path format
    
    df = pd.read_csv(data_path)
    return df
