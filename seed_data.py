from app import create_app, db
from app.models import ClimateRecord
import csv

app = create_app()
app.app_context().push()

with open('datasets/processed/narok_climate_30yrs_expanded.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        record = ClimateRecord(
            year=int(row['year']),
            month=int(row['month']),
            temperature=float(row['temperature']),
            rainfall=float(row['rainfall']),
            humidity=float(row['humidity']),
            wind_speed=float(row['wind_speed']),
            solar_radiation=float(row['solar_radiation']),
            evapotranspiration=float(row['evapotranspiration']),
            soil_moisture=float(row['soil_moisture']),
            cloud_cover=float(row['cloud_cover']),
            air_pressure=float(row['air_pressure']),
            dew_point=float(row['dew_point']),
            min_temperature=float(row['min_temperature']),
            max_temperature=float(row['max_temperature']),
            vegetation_index=float(row['vegetation_index']),
            heat_index=float(row['heat_index']),
            drought_index=float(row['drought_index']),
            CO2_concentration=float(row['CO2_concentration'])
        )
        db.session.add(record)

    db.session.commit()
    print("Data seeding complete.")
