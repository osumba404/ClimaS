# Current: Predict temp, rainfall, humidity, and simulate "deforestation factor"

# We Can Add:
# Predict extreme weather likelihood (heatwaves, drought probability)
# Feature importance graph (what's driving the climate most?)
# Trend uncertainty ranges (best & worst-case projections)
# Regional comparison (compare two regions side by side)
# Save user simulation scenarios






# app/ml_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ------------------------------------------
# Load Sample Climate Data
# In production, replace with real datasets or APIs
# ------------------------------------------
def load_sample_data():
    """
    Simulates historical climate data.
    Returns:
        pd.DataFrame: Climate dataset with Year, Temperature, Rainfall, Humidity
    """
    data = {
        'Year': range(2000, 2025),
        'Temperature': [25.0 + i * 0.1 + np.random.normal(0, 0.5) for i in range(25)],
        'Rainfall': [800 + i * 2 + np.random.normal(0, 50) for i in range(25)],
        'Humidity': [60 + i * 0.5 + np.random.normal(0, 5) for i in range(25)]
    }
    return pd.DataFrame(data)


# ------------------------------------------
# Train ML Model
# ------------------------------------------
def train_model(df):
    """
    Trains a Random Forest model for each climate target.
    Args:
        df (pd.DataFrame): Historical climate dataset
    Returns:
        dict: Trained models for Temperature, Rainfall, Humidity
    """
    models = {}
    X = df[['Year']]

    for target in ['Temperature', 'Rainfall', 'Humidity']:
        y = df[target]
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        models[target] = model

    return models


# ------------------------------------------
# Predict Future Climate Conditions
# ------------------------------------------
def predict_climate(models, years_ahead):
    """
    Predicts future climate metrics based on trained models.
    Args:
        models (dict): Trained models
        years_ahead (int): Number of years to forecast
    Returns:
        pd.DataFrame: Predicted climate for future years
    """
    future_years = np.array(range(2025, 2025 + years_ahead)).reshape(-1, 1)
    predictions = {}

    for target, model in models.items():
        predictions[target] = model.predict(future_years)

    return pd.DataFrame({
        'Year': range(2025, 2025 + years_ahead),
        'Temperature': predictions['Temperature'],
        'Rainfall': predictions['Rainfall'],
        'Humidity': predictions['Humidity']
    })


# ------------------------------------------
# Simulate Scenario: Deforestation Impact
# ------------------------------------------
def simulate_scenario(df, deforestation_factor):
    """
    Applies deforestation effects to predicted climate.
    Args:
        df (pd.DataFrame): Baseline predicted climate
        deforestation_factor (float): 0.0 to 1.0 scale representing % deforestation
    Returns:
        pd.DataFrame: Adjusted climate data reflecting deforestation impact
    """
    df_simulated = df.copy()

    # +0.5°C per 10% deforestation
    df_simulated['Temperature'] += deforestation_factor * 0.5  

    # -20% rainfall per 10% deforestation
    df_simulated['Rainfall'] *= (1 - deforestation_factor * 0.2)  

    return df_simulated
