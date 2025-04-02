from flask import Blueprint, request, jsonify
from app.controllers.ContactoControllers import (
    registrarContacto,
    verificarEmail,
    login,  
    listarContactos,
    eliminarContacto,
    editarContacto,
)

# Crear el Blueprint para los contactos
contactosRuta = Blueprint('contactos', __name__)

# Ruta para registrar un nuevo contacto
@contactosRuta.route('/registrar', methods=['POST'])
def registrar():
    data = request.json  
    response, status_code = registrarContacto(data)
    return jsonify(response), status_code

@contactosRuta.route('/verificar/<token>', methods=['GET'])
def verificar(token):
    response, status_code = verificarEmail(token)
    return jsonify(response), status_code

# Ruta para iniciar sesión
@contactosRuta.route('/login', methods=['POST'])
def iniciar_sesion():
    data = request.json
    response, status_code = login(data)
    return jsonify(response), status_code

# Ruta para obtener todos los contactos registrados
@contactosRuta.route('/listar', methods=['GET'])
def obtener_contactos():
    response, status_code = listarContactos()
    return jsonify(response), status_code

# Ruta para eliminar un contacto por id
@contactosRuta.route('/contacto/<contactoid>', methods=['DELETE'])
def eliminar(contactoid):
    # Convertir el id de string a ObjectId
    from bson import ObjectId
    try:
        contactoid = ObjectId(contactoid)
    except Exception as e:
        return jsonify({"error": "ID de contacto no válido"}), 400
    
    response, status_code = eliminarContacto(contactoid)
    return jsonify(response), status_code

# Ruta para editar un contacto por id
@contactosRuta.route('/contacto/<contactoid>', methods=['PUT'])
def editar(contactoid):
    # Convertir el id de string a ObjectId
    from bson import ObjectId
    try:
        contactoid = ObjectId(contactoid)
    except Exception as e:
        return jsonify({"error": "ID de contacto no válido"}), 400
    
    datos_actualizados = request.json  
    response, status_code = editarContacto(contactoid, datos_actualizados)
    return jsonify(response), status_code