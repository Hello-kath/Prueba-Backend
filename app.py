from flask import Flask, jsonify
from app.config import Config
from app.DB.DBconnection import connectionMongo
from app.routes.contactos_routes import contactos_bp 

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar configuraciones desde config.py
app.config.from_object(Config)

# Registrar las rutas (puedes tener múltiples Blueprints o rutas)
app.register_blueprint(contactos_bp, url_prefix='/contactos')

# Punto de entrada principal
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
