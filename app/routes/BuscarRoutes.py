from flask import Blueprint, request, jsonify
from app.controllers.BuscarController import buscarContacto

# Crear el Blueprint para la búsqueda
buscarContR = Blueprint('buscar', __name__)  

# Ruta para buscar contactos por nombre o número
@buscarContR.route('/buscarC', methods=['GET'])  
def buscar():
    # Obtener el parámetro 'termino' de la URL
    termino = request.args.get("termino")

    # Validar que se proporcionó un término de búsqueda
    if not termino:
        return jsonify({"error": "El parámetro 'termino' es requerido"}), 400

    # Llamar a la función que busca el contacto
    response, status_code = buscarContacto(termino)
    return jsonify(response), status_code
