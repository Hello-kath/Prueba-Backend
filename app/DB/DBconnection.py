import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de MongoDB desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")

# Funcion para conectar a MongoDB
def connectionMongo():
    try:
        # Crear una instancia del cliente MongoDB usando la URI
        client = MongoClient(MONGO_URI)
        
        # Obtener la base de datos
        db = client.get_database()  # Esto obtiene la base de datos por defecto
        return db
    
    except Exception as e:
        print(f"Error al conectar con la base de datos MongoDB: {e}")
        return None
