from scripts.constants.app_constants import AppConstants
import os
from dotenv import load_dotenv

load_dotenv('.env')


class AppConfig:
    DATABASE_HOST = os.getenv("DB_HOST")
    DATABASE_PORT = os.getenv("DB_PORT")
    DATABASE_USER = os.getenv("DB_USER")
    DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE_NAME = os.getenv("DB_NAME")

    API_HOST = os.getenv("API_HOST")
    API_PORT = os.getenv("API_PORT")

STARTUP_MESSAGE = AppConstants.SUCCESS_MESSAGE