from werkzeug.security import generate_password_hash, check_password_hash
from app.DB.DBconnection import connectionMongo
from app.config import Config
import jwt
import os
import smtplib
from bson import ObjectId
from email.mime.text import MIMEText


# Función para registrar un contacto
from werkzeug.security import generate_password_hash
from app.DB.DBconnection import connectionMongo
from app.config import Config
import jwt
import smtplib
from email.mime.text import MIMEText

def registrarContacto(data):
    try:
        # Extraer datos del request
        nombre = data.get("nombreContacto")
        telefono = data.get("numTelefono")
        correo = data.get("correo")
        password = data.get("password")
        confirmPassword = data.get("confirmPassword")
        
        # verificar que los campos esten
        if not nombre or not telefono or not correo or not password or not confirmPassword:
            return {"error": "Todos los campos son obligatorios"}, 400
            
        if password != confirmPassword:
            return {"error": "Las contraseñas no coinciden"}, 400

        # Conectar a la base de datos
        db = connectionMongo()
        if db is None:
            return {"error": "Error de conexión con la base de datos"}, 500

        # Crear nuevo contacto
        db.Contactos.insert_one({
            "nombreContacto": nombre,
            "numTelefono": telefono,
            "correo": correo,
            "password": generate_password_hash(password),
            "verificado": False
        })

        # Generar token y enviar correo
        token = jwt.encode({"correo": correo}, str(Config.JWT_SECRET), algorithm="HS256")
        
        try:
            # Enviar correo simple
            msg = MIMEText(f"Verifica tu cuenta: http://localhost:5000/contactos/verificar/{token}")
            msg['Subject'] = "Confirma tu correo"
            msg['From'] = Config.EMAIL
            msg['To'] = correo
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(Config.EMAIL, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return {"mensaje": "Registro exitoso. Error al enviar correo de confirmación."}, 201

        return {"mensaje": "Registro exitoso. Verifica tu correo."}, 201
        
    except Exception as e:
        print(f"Error en registro: {e}")
        return {"error": "Error al procesar el registro"}, 500

#-----------------------------------------------------------------------------------------------------

# Función para enviar correo de confirmacion 
def verificarEmail(token):
    try:
        # Decodificar el token
        decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        
        # Obtener el correo del token decodificado
        correo = decoded.get("correo")
        if not correo:
            return {"error": "Token inválido: no contiene información de correo"}, 400
        
        # Conectar a la base de datos
        db = connectionMongo()
        if db is None:
            return {"error": "Error de conexión con la base de datos"}, 500
        
        # Buscar el usuario por correo
        usuario = db.Contactos.find_one({"correo": correo})
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404
        
        # Actualizar el estado de verificación del usuario
        resultado = db.Contactos.update_one(
            {"correo": correo},
            {"$set": {"verificado": True}}
        )
        
        # Verificar que la actualización fue exitosa
        if resultado.modified_count == 0:
            return {"error": "No se pudo actualizar el estado de verificación"}, 500
        
        return {"mensaje": "Correo verificado exitosamente"}, 200
        
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado"}, 400
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}, 400
    except Exception as e:
        print(f"Error al verificar correo: {str(e)}")
        return {"error": "Ocurrió un error durante la verificación"}, 500

#------------------------------------------------------------------------------------------

# Función para iniciar sesion
def login(data):
    correo = data.get("correo")
    password = data.get("password")
    
    # Validar datos
    if not correo or not password:
        return {"error": "Correo y contraseña son obligatorios"}, 400

    # Conectar a la base de datos
    db = connectionMongo()
    if db is None:
        return {"error": "Error de conexión con la base de datos"}, 500

    # Buscar usuario
    usuario = db.Contactos.find_one({"correo": correo})
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
        
    # Verificar contraseña
    if not check_password_hash(usuario["password"], password):
        return {"error": "Contraseña incorrecta"}, 401

    # Generar token
    token = jwt.encode({"correo": correo}, Config.JWT_SECRET, algorithm="HS256")

    return {"mensaje": "Login exitoso", "token": token}, 200


#------------------------------------------------------------------------------------------------

# Función para obtener todos los contactos registrados
def listarContactos():
    # Conectar a la base de datos
    db = connectionMongo()
    if db is None:
        return {"error": "Error de conexión con la base de datos"}, 500

    # Obtener todos los contactos 
    contactos = db.Contactos.find({}, {"_id": 1, "password": 0}).sort("nombreContacto", 1)    

    # Convertir los resultados a una lista
    contactosList = [
            {**contacto, "_id": str(contacto["_id"])} for contacto in contactos
        ]

    if not contactosList:
        return {"error": "No hay contactos registrados"}, 404

    return {"contactos": contactosList}, 200


#-------------------------------------------------------------------------------------------

# Función para eliminar un contacto
def eliminarContacto(contactoid):
    # Conectar a la base de datos
    db = connectionMongo()
    if db is None:
        return {"error": "Error de conexión con la base de datos"}, 500

    # Buscar el contacto por id
    contacto = db.Contactos.find_one({"_id": contactoid})
    if not contacto:
        return {"error": "Contacto no encontrado"}, 404

    # Eliminar el contacto de la base de datos
    db.Contactos.delete_one({"_id": contactoid})

    return {"mensaje": "Contacto eliminado"}, 200


#------------------------------------------------------------------------------------------

# Función para editar un contacto por _id
def editarContacto(contactoid, datosActualizados):
    # Conectar a la base de datos
    db = connectionMongo()
    if db is None:
        return {"error": "Error de conexión con la base de datos"}, 500

    # Buscar el contacto por id
    contacto = db.Contactos.find_one({"_id": contactoid})
    if not contacto:
        return {"error": "contacto no encontrado"}, 404

    # Actualizar el contacto con los nuevos datos
    db.Contactos.update_one({"_id": contactoid}, {"$set": datosActualizados})

    return {"mensaje": "contacto actualizado exitosamente"}, 200
