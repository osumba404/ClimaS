# app/data_utils.py

import pandas as pd
import numpy as np

from app.models import ClimateRecord

def load_historical_data():
    """
    Loads full climate records from DB as DataFrame with all features.
    """
    records = ClimateRecord.query.order_by(ClimateRecord.year, ClimateRecord.month).all()

    data = [{
        'Year': rec.year,
        'Month': rec.month,
        'Temperature': rec.temperature,
        'Rainfall': rec.rainfall,
        'Humidity': rec.humidity,
        'WindSpeed': rec.wind_speed,
        'SolarRadiation': rec.solar_radiation,
        'Evapotranspiration': rec.evapotranspiration,
        'SoilMoisture': rec.soil_moisture,
        'CloudCover': rec.cloud_cover,
        'AirPressure': rec.air_pressure,
        'DewPoint': rec.dew_point,
        'MinTemperature': rec.min_temperature,
        'MaxTemperature': rec.max_temperature,
        'VegetationIndex': rec.vegetation_index,
        'HeatIndex': rec.heat_index,
        'DroughtIndex': rec.drought_index,
        'CO2Concentration': rec.CO2_concentration
    } for rec in records]

    return pd.DataFrame(data)

