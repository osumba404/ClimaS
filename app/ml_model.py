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
