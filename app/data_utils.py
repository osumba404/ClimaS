# climas/app/data_utils.py
import pandas as pd
import numpy as np
import os

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, '..', 'datasets', 'processed')
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "processed_climate_data.csv")

def generate_synthetic_data():
    """Generates a realistic synthetic climate dataset and saves it."""
    print("Generating synthetic climate data...")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    date_rng = pd.date_range(start='2004-01-01', end='2023-12-31', freq='M')
    df = pd.DataFrame(date_rng, columns=['date'])
    
    # Simulate features
    df['temperature'] = 22 + np.sin(np.pi * df['date'].dt.month / 6) * 6 + \
                        (df['date'].dt.year - 2004) * 0.06 + np.random.randn(len(df)) * 0.4
    df['rainfall'] = 90 + np.sin(np.pi * df['date'].dt.month / 6 + 1.5) * 50 + np.random.randn(len(df)) * 25
    df['rainfall'] = df['rainfall'].clip(0)
    df['humidity'] = 75 - (df['temperature'] - 22) * 2.5 + np.random.randn(len(df)) * 5
    df['humidity'] = df['humidity'].clip(30, 98)
    df['land_use_proxy'] = np.linspace(0.2, 0.5, len(df)) + np.random.rand(len(df)) * 0.05
    df['temperature'] += df['land_use_proxy'] * 3

    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Synthetic data saved to {PROCESSED_DATA_PATH}")
    return df

def load_processed_data():
    """Loads the processed data file into a pandas DataFrame."""
    if not os.path.exists(PROCESSED_DATA_PATH):
        generate_synthetic_data()
    return pd.read_csv(PROCESSED_DATA_PATH, parse_dates=['date'])