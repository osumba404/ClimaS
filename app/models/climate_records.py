from app.models import db

class ClimateRecord(db.Model):
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
        return f"<ClimateRecord {self.year}-{self.month}>"
