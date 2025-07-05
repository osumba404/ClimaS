# climas/app/config.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    """Set Flask configuration from .env file."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'