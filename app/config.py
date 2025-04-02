import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde .env

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    EMAIL = os.getenv("EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", False)  # Valor predeterminado False si no se encuentra