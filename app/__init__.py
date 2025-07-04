# climas/app/__init__.py
from flask import Flask
from .config import Config
from . import data_utils
import os

def create_app(config_class=Config):
    """
    Creates and configures the Flask application.
    This is the application factory.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- First-time setup: Generate data and train model if they don't exist ---
    if not os.path.exists(data_utils.PROCESSED_DATA_PATH):
        print("Processed data not found. Generating new synthetic data...")
        data_utils.generate_synthetic_data()

    from . import ml_model
    if not os.path.exists(ml_model.MODEL_PATH):
        print("ML model not found. Training a new model...")
        ml_model.train_model()

    # --- Register routes ---
    from . import routes
    app.register_blueprint(routes.main_bp)

    print("ClimaS application created successfully.")
    return app
