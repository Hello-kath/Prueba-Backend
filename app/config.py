import os

class Config:
    # Clave secreta para generar y verificar tokens JWT
    JWT_SECRET = os.getenv("JWT_SECRET")
    
    # Configuración para enviar correos electrónicos desde la API
    EMAIL = os.getenv("EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # Otras configuraciones 
    DEBUG = os.getenv("FLASK_DEBUG") == "True"  

