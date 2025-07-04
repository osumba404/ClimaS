from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    # Dynamic paths (optional, but robust)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__,
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))

    # app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET', 'default_secret')

    from .routes import main
    app.register_blueprint(main)

    return app
