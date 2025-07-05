from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .climate_record import ClimateRecord

import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('config.Config')

    db.init_app(app)

    # Import models so SQLAlchemy knows them
    from app.models.climate_record import ClimateRecord

    # Register routes blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
