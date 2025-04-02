from flask import Flask, jsonify
from app.config import Config
from app.DB.DBconnection import connectionMongo
from app.routes.ContactoRoutes import contactosRuta
from app.routes.BuscarRoutes import buscarContR 

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar configuraciones desde config.py
app.config.from_object(Config)

# Registrar las rutas 
app.register_blueprint(contactosRuta, url_prefix='/contactos')
app.register_blueprint(buscarContR, url_prefix='/buscar')

# Punto de entrada principal
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
