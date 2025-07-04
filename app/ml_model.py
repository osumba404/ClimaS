# Current: Predict temp, rainfall, humidity, and simulate "deforestation factor"

# We Can Add:
# Predict extreme weather likelihood (heatwaves, drought probability)
# Feature importance graph (what's driving the climate most?)
# Trend uncertainty ranges (best & worst-case projections)
# Regional comparison (compare two regions side by side)
# Save user simulation scenarios






# app/ml_model.py

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# ===============================
# Train Random Forest models
# ===============================
def train_model(df):
    """
    Trains separate Random Forest models for Temperature, Rainfall, and Humidity.
    
    Args:
        df (DataFrame): Historical climate data with 'Year', 'Temperature', 'Rainfall', 'Humidity' columns.
    
    Returns:
        dict: Dictionary of trained models {'Temperature': model, 'Rainfall': model, 'Humidity': model}
    """
    X = df[['Year']]
    models = {}

    for target in ['Temperature', 'Rainfall', 'Humidity']:
        y = df[target]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        models[target] = model

    return models


# ===============================
# Predict Future Climate
# ===============================
def predict_climate(models, years_ahead, start_year=2025):
    """
    Predicts future climate trends using trained models.

    Args:
        models (dict): Trained models for each target variable.
        years_ahead (int): Number of years to predict.
        start_year (int): Year to start predictions from.

    Returns:
        DataFrame: Predicted 'Year', 'Temperature', 'Rainfall', 'Humidity' values.
    """
    future_years = np.arange(start_year, start_year + years_ahead).reshape(-1, 1)
    predictions = {}

    for target, model in models.items():
        predictions[target] = model.predict(future_years)

    predicted_df = pd.DataFrame({
        'Year': future_years.flatten(),
        'Temperature': predictions['Temperature'],
        'Rainfall': predictions['Rainfall'],
        'Humidity': predictions['Humidity']
    })

    return predicted_df


# ===============================
# Simulate Scenario (e.g., deforestation impact)
# ===============================
def simulate_scenario(df, deforestation_factor):
    """
    Simulates climate impact of deforestation by adjusting temperature and rainfall.

    Args:
        df (DataFrame): Predicted climate DataFrame.
        deforestation_factor (float): Percentage increase in deforestation (0.0 - 1.0 scale).

    Returns:
        DataFrame: Adjusted climate DataFrame after simulation.
    """
    df_simulated = df.copy()
    df_simulated['Temperature'] += deforestation_factor * 0.5  # +0.5°C per 10% deforestation
    df_simulated['Rainfall'] *= (1 - deforestation_factor * 0.2)  # -20% rainfall per 10% deforestation

    return df_simulated
