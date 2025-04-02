from app.DB.DBconnection import connectionMongo


# Función para buscar un contacto por nombre o número
def buscarContacto(datoBuscar):
    # Conectar a la base de datos
    db = connectionMongo()
    if db is None:
        return {"error": "Error de conexión con la base de datos"}, 500
    
    # Convertir el término de búsqueda a string y eliminar espacios extra
    datoBuscar = str(datoBuscar).strip()
    
    # Crear la consulta para buscar por nombre o número exactamente
    consulta = {
        "$or": [
            {"nombreContacto": datoBuscar},  # Búsqueda exacta por nombre
            {"numTelefono": datoBuscar}  # Búsqueda exacta por número
        ]
    }
    
    # Buscar contactos que coincidan con la consulta
    contactos = list(db.Contactos.find(consulta, {"correo": 1, "nombreContacto": 1, "numTelefono": 1, "_id": 0}))

    
    # Si no se encontraron contactos
    if not contactos:
        return {"error": "No se encontraron contactos con ese nombre o número"}, 404
    
    # Convertir ObjectId a string para serialización JSON
    for contacto in contactos:
        if "_id" in contacto:
            contacto["_id"] = str(contacto["_id"])
    
    return {"contactos": contactos}, 200