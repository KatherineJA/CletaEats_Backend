from logica.auth_service import AuthService

auth_service = AuthService()


def manejar_post(path, body, responder):

    if path == "/login":
        correo   = body.get("correo")
        password = body.get("password")
        if not correo or not password:
            responder(400, {"exito": False, "mensaje": "Correo y contrasena requeridos"})
            return True
        responder(200, auth_service.login(correo, password))
        return True

    elif path == "/registro/cliente":
        campos_obligatorios = ["cedula", "nombre", "correo", "password", "telefono"]
        if not all(body.get(c) for c in campos_obligatorios):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, auth_service.registrar_cliente(
            body["cedula"], body["nombre"], body["correo"], body["password"],
            body["telefono"],
            body.get("numero_tarjeta", ""),
            body.get("latitud"), body.get("longitud")
        ))
        return True

    elif path == "/registro/repartidor":
        campos_obligatorios = ["cedula", "nombre", "correo", "password", "telefono"]
        if not all(body.get(c) for c in campos_obligatorios):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, auth_service.registrar_repartidor(
            body["cedula"], body["nombre"], body["correo"], body["password"],
            body["telefono"],
            body.get("numero_tarjeta", ""),          # opcional
            body.get("latitud"), body.get("longitud")
        ))
        return True

    elif path == "/auth/recuperar":
        correo_o_tel = body.get("correo_o_telefono")
        metodo       = body.get("metodo", "email")
        if not correo_o_tel:
            responder(400, {"exito": False, "mensaje": "correo_o_telefono requerido"})
            return True
        if metodo not in ("email", "sms"):
            responder(400, {"exito": False, "mensaje": "metodo debe ser 'email' o 'sms'"})
            return True
        responder(200, auth_service.solicitar_recuperacion(correo_o_tel, metodo))
        return True

    elif path == "/auth/verificar-codigo":
        correo_o_tel = body.get("correo_o_telefono")
        codigo       = body.get("codigo")
        if not correo_o_tel or not codigo:
            responder(400, {"exito": False, "mensaje": "correo_o_telefono y codigo requeridos"})
            return True
        responder(200, auth_service.verificar_codigo(correo_o_tel, codigo))
        return True

    elif path == "/auth/cambiar-password":
        correo_o_tel  = body.get("correo_o_telefono")
        codigo        = body.get("codigo")
        nueva_pass    = body.get("nueva_password")
        if not correo_o_tel or not codigo or not nueva_pass:
            responder(400, {"exito": False,
                            "mensaje": "correo_o_telefono, codigo y nueva_password requeridos"})
            return True
        responder(200, auth_service.cambiar_password(correo_o_tel, codigo, nueva_pass))
        return True

    return False
