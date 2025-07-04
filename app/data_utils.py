# app/data_utils.py

import pandas as pd
import numpy as np

# ===============================
# Load Sample Historical Climate Data
# ===============================
def load_sample_data():
    """
    Generates simulated historical climate data.
    Replace with real API or datasets in production.

    Returns:
        DataFrame: Historical climate trends (2000 - 2024)
    """
    years = np.arange(2000, 2025)
    data = {
        'Year': years,
        'Temperature': 25 + 0.1 * (years - 2000) + np.random.normal(0, 0.5, len(years)),
        'Rainfall': 800 + 2 * (years - 2000) + np.random.normal(0, 50, len(years)),
        'Humidity': 60 + 0.5 * (years - 2000) + np.random.normal(0, 5, len(years))
    }

    return pd.DataFrame(data)
