<<<<<<< HEAD
# climas/app/ml_model.py
import pandas as pd
import numpy as np
import joblib
import os
import plotly
import plotly.graph_objs as go
import json
from sklearn.ensemble import RandomForestRegressor
from . import data_utils

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, "climate_models.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "model_features.pkl")

# --- Model Training and Loading ---
def train_model():
    """Trains ML models on processed data and saves them."""
    print("Initiating model training...")
    df = data_utils.load_processed_data()
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    features = ['year', 'month', 'land_use_proxy']
    targets = ['temperature', 'rainfall', 'humidity']
    
    X = df[features]
    y = df[targets]
    
    models = {}
    for target in targets:
        print(f"Training model for: {target}")
        model = RandomForestRegressor(n_estimators=150, random_state=42, min_samples_leaf=3)
        model.fit(X, y[target])
        models[target] = model
        
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(models, MODEL_PATH)
    joblib.dump(features, FEATURES_PATH)
    print(f"Model training complete. Models saved to {MODEL_PATH}")

def load_model_and_artifacts():
    """Loads trained models and feature list."""
    if not all([os.path.exists(MODEL_PATH), os.path.exists(FEATURES_PATH)]):
        train_model()
    models = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    return models, features

# --- Prediction and Simulation ---
def predict_future_climate(models, features, start_year, end_year, simulation_params=None):
    """Predicts future climate for a given time range and simulation scenario."""
    if simulation_params is None: simulation_params = {}
    future_dates = pd.date_range(start=f'{start_year}-01-01', end=f'{end_year}-12-31', freq='M')
    future_df = pd.DataFrame(future_dates, columns=['date'])
    future_df['year'] = future_df['date'].dt.year
    future_df['month'] = future_df['date'].dt.month
    
    historical_df = data_utils.load_processed_data()
    last_known_land_use = historical_df['land_use_proxy'].iloc[-1]
    land_use_change = simulation_params.get('land_use_change', 0.0)
    final_land_use = last_known_land_use * (1 + land_use_change)
    future_df['land_use_proxy'] = np.linspace(last_known_land_use, final_land_use, len(future_df))
    
    X_future = future_df[features]
    for target, model in models.items():
        future_df[f'predicted_{target}'] = model.predict(X_future)
    return future_df

# --- Visualization Functions ---
def to_json(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
=======
# # Current: Predict temp, rainfall, humidity, and simulate "deforestation factor"

# # We Can Add:
# # Predict extreme weather likelihood (heatwaves, drought probability)
# # Feature importance graph (what's driving the climate most?)
# # Trend uncertainty ranges (best & worst-case projections)
# # Regional comparison (compare two regions side by side)
# # Save user simulation scenarios





# # app/ml_model.py

# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestRegressor
# from app.models import ClimateRecord
# import warnings

# warnings.filterwarnings("ignore")  # Optional: Clean up random sklearn warnings


# # ------------------------------------------
# # Load Data from SQLite (via SQLAlchemy)
# # ------------------------------------------
# def load_real_data():
#     """
#     Loads real historical climate data from the database.
#     Returns:
#         pd.DataFrame: Yearly average climate metrics
#     """
#     records = ClimateRecord.query.all()

#     data = [{
#         'Year': r.year,
#         'Month': r.month,
#         'Temperature': r.temperature,
#         'Rainfall': r.rainfall,
#         'Humidity': r.humidity
#     } for r in records]

#     df = pd.DataFrame(data)

#     # Group by Year for yearly averages
#     df = df.groupby('Year').mean().reset_index()

#     return df


# # ------------------------------------------
# # Train ML Models for Each Metric
# # ------------------------------------------
# def train_model(df):
#     """
#     Trains separate Random Forest models for Temp, Rainfall, Humidity.
#     Args:
#         df (pd.DataFrame): Historical climate data
#     Returns:
#         dict: Trained models
#     """
#     models = {}
#     X = df[['Year']]  # Feature: just year for now

#     for target in ['Temperature', 'Rainfall', 'Humidity']:
#         y = df[target]
#         model = RandomForestRegressor(n_estimators=100, random_state=42)
#         model.fit(X, y)
#         models[target] = model

#     return models


# # ------------------------------------------
# # Predict Future Climate for N Years
# # ------------------------------------------
# def predict_climate(models, years_ahead):
#     """
#     Forecasts temperature, rainfall, and humidity for future years.
#     Args:
#         models (dict): Trained models
#         years_ahead (int): Years to forecast
#     Returns:
#         pd.DataFrame: Predicted metrics
#     """
#     future_years = np.array(range(2025, 2025 + years_ahead)).reshape(-1, 1)
#     predictions = {}

#     for target, model in models.items():
#         predictions[target] = model.predict(future_years)

#     return pd.DataFrame({
#         'Year': range(2025, 2025 + years_ahead),
#         'Temperature': predictions['Temperature'],
#         'Rainfall': predictions['Rainfall'],
#         'Humidity': predictions['Humidity']
#     })
>>>>>>> 79d45465cf3a2ef4c3330698045f2fbdd6de00cd

def create_historical_plots(df_hist):
    """Creates JSON for historical data plots."""
    trace_temp = go.Scatter(x=df_hist['date'], y=df_hist['temperature'], mode='lines', name='Avg Temperature')
    layout_temp = go.Layout(title='Historical Temperature Trend', yaxis_title='Temperature (°C)')
    fig_temp = go.Figure(data=[trace_temp], layout=layout_temp)

<<<<<<< HEAD
    trace_rain = go.Bar(x=df_hist['date'], y=df_hist['rainfall'], name='Monthly Rainfall')
    layout_rain = go.Layout(title='Historical Rainfall Patterns', yaxis_title='Rainfall (mm)')
    fig_rain = go.Figure(data=[trace_rain], layout=layout_rain)
    
    return {'temp': to_json(fig_temp), 'rain': to_json(fig_rain)}

def create_feature_importance_plot(models, features):
    """Creates JSON for feature importance plot."""
    importances = models['temperature'].feature_importances_
    fig = go.Figure([go.Bar(x=features, y=importances)])
    fig.update_layout(title_text='Key Climate Drivers (Feature Importance)', yaxis_title='Importance')
    return to_json(fig)

def create_simulation_comparison_plot(baseline_df, simulated_df):
    """Creates JSON for the simulation comparison plot."""
    trace_base = go.Scatter(x=baseline_df['date'], y=baseline_df['predicted_temperature'], mode='lines', name='Baseline Temp', line=dict(dash='dash'))
    trace_sim = go.Scatter(x=simulated_df['date'], y=simulated_df['predicted_temperature'], mode='lines', name='Simulated Temp', line=dict(color='red'))
    layout_sim = go.Layout(title='Temperature: Baseline vs. Simulated Scenario', yaxis_title='Temperature (°C)')
    fig_sim = go.Figure(data=[trace_base, trace_sim], layout=layout_sim)
    return to_json(fig_sim)
=======
# # ------------------------------------------
# # Simulate Deforestation Scenario
# # ------------------------------------------
# def simulate_scenario(df, deforestation_factor):
#     """
#     Simulates the effect of deforestation on predicted climate.
#     Args:
#         df (pd.DataFrame): Predicted climate (baseline)
#         deforestation_factor (float): Scale from 0 to 1
#     Returns:
#         pd.DataFrame: Adjusted climate projections
#     """
#     df_simulated = df.copy()

#     # +0.5°C per 10% deforestation
#     df_simulated['Temperature'] += deforestation_factor * 0.5

#     # -20% rainfall per 10% deforestation
#     df_simulated['Rainfall'] *= (1 - deforestation_factor * 0.2)

#     return df_simulated


# # ------------------------------------------
# # Optional: Get Feature Importance
# # ------------------------------------------
# def get_feature_importance(model, feature_names=['Year']):
#     """
#     Extracts feature importances from a trained model.
#     Args:
#         model (RandomForestRegressor)
#     Returns:
#         dict: Feature importances
#     """
#     importances = model.feature_importances_
#     return dict(zip(feature_names, importances))





from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClimateRecord(db.Model):
    __tablename__ = 'climate_records'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)

    temperature = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    solar_radiation = db.Column(db.Float)
    evapotranspiration = db.Column(db.Float)
    soil_moisture = db.Column(db.Float)
    cloud_cover = db.Column(db.Float)
    air_pressure = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    min_temperature = db.Column(db.Float)
    max_temperature = db.Column(db.Float)
    vegetation_index = db.Column(db.Float)
    heat_index = db.Column(db.Float)
    drought_index = db.Column(db.Float)
    CO2_concentration = db.Column(db.Float)

    def __repr__(self):
        return f'<ClimateRecord {self.year}-{self.month}>'
>>>>>>> 79d45465cf3a2ef4c3330698045f2fbdd6de00cd
