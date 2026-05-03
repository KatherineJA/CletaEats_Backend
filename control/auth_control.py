from logica.auth_service import AuthService

auth_service = AuthService()


def manejar_post(path, body, responder):
    if path == "/login":
        correo = body.get("correo")
        password = body.get("password")
        if not correo or not password:
            responder(400, {"exito": False, "mensaje": "Correo y contraseña requeridos"})
            return True
        responder(200, auth_service.login(correo, password))
        return True

    elif path == "/registro/cliente":
        campos = ["cedula", "nombre", "correo", "password", "telefono", "numero_tarjeta"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, auth_service.registrar_cliente(
            body["cedula"], body["nombre"], body["correo"], body["password"],
            body["telefono"], body["numero_tarjeta"],
            body.get("latitud"), body.get("longitud")
        ))
        return True

    elif path == "/registro/repartidor":
        campos = ["cedula", "nombre", "correo", "password", "telefono", "numero_tarjeta"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, auth_service.registrar_repartidor(
            body["cedula"], body["nombre"], body["correo"], body["password"],
            body["telefono"], body["numero_tarjeta"],
            body.get("latitud"), body.get("longitud")
        ))
        return True

    return False