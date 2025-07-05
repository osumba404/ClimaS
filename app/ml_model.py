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

def create_historical_plots(df_hist):
    """Creates JSON for historical data plots."""
    trace_temp = go.Scatter(x=df_hist['date'], y=df_hist['temperature'], mode='lines', name='Avg Temperature')
    layout_temp = go.Layout(title='Historical Temperature Trend', yaxis_title='Temperature (°C)')
    fig_temp = go.Figure(data=[trace_temp], layout=layout_temp)

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
