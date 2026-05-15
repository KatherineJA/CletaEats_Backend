from logica.usuario_service import UsuarioService

usuario_service = UsuarioService()


def manejar_post(path, body, responder):
    if path == "/usuario/perfil":
        id_usuario = body.get("id_usuario")
        telefono = body.get("telefono")
        if not id_usuario or not telefono:
            responder(400, {"exito": False, "mensaje": "id_usuario y telefono requeridos"})
            return True
        responder(200, usuario_service.editar_perfil(
            id_usuario, telefono, body.get("latitud"), body.get("longitud")
        ))
        return True

    elif path == "/usuario/tarjeta/cliente":
        id_usuario = body.get("id_usuario")
        numero_tarjeta = body.get("numero_tarjeta")
        if not id_usuario or not numero_tarjeta:
            responder(400, {"exito": False, "mensaje": "id_usuario y numero_tarjeta requeridos"})
            return True
        responder(200, usuario_service.editar_tarjeta_cliente(id_usuario, numero_tarjeta))
        return True

    elif path == "/usuario/tarjeta/repartidor":
        id_usuario = body.get("id_usuario")
        numero_tarjeta = body.get("numero_tarjeta")
        if not id_usuario or not numero_tarjeta:
            responder(400, {"exito": False, "mensaje": "id_usuario y numero_tarjeta requeridos"})
            return True
        responder(200, usuario_service.editar_tarjeta_repartidor(id_usuario, numero_tarjeta))
        return True

    elif path == "/usuario/reactivar/cliente":
        id_usuario = body.get("id_usuario")
        if not id_usuario:
            responder(400, {"exito": False, "mensaje": "id_usuario requerido"})
            return True
        responder(200, usuario_service.reactivar_cliente(id_usuario))
        return True

    elif path == "/usuario/reactivar/repartidor":
        id_usuario = body.get("id_usuario")
        if not id_usuario:
            responder(400, {"exito": False, "mensaje": "id_usuario requerido"})
            return True
        responder(200, usuario_service.reactivar_repartidor(id_usuario))
        return True



    elif path == "/usuario/foto":
        import base64, os
        id_usuario = body.get("id_usuario")
        foto_b64 = body.get("foto_base64")
        if not id_usuario or not foto_b64:
            responder(400, {"exito": False, "mensaje": "Faltan datos"})
            return True
        try:
            usar_imgbb = os.environ.get("USAR_IMGBB", "false").lower() == "true"
            if usar_imgbb:
                import requests
                IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY", "")
                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": IMGBB_API_KEY, "image": foto_b64}
                )
                resultado = response.json()
                if resultado.get("success"):
                    url = resultado["data"]["url"]
                    usuario_service.guardar_url_foto(id_usuario, url)
                    responder(200, {"exito": True, "url": url})
                else:
                    responder(500, {"exito": False, "mensaje": "Error al subir imagen a ImgBB"})
            else:
                datos = base64.b64decode(foto_b64)
                carpeta = "fotos_perfil"
                os.makedirs(carpeta, exist_ok=True)
                ruta = f"{carpeta}/usuario_{id_usuario}.jpg"
                with open(ruta, "wb") as f:
                    f.write(datos)
                url = f"/fotos_perfil/usuario_{id_usuario}.jpg"
                usuario_service.guardar_url_foto(id_usuario, url)
                responder(200, {"exito": True, "url": url})

        except Exception as e:

            responder(500, {"exito": False, "mensaje": str(e)})

        return True


def manejar_get(path, query, responder):
    if path == "/usuario/perfil":
        id_usuario = query.get("id", [None])[0]
        if not id_usuario:
            responder(400, {"exito": False, "mensaje": "id requerido"})
            return True
        responder(200, usuario_service.obtener_perfil(int(id_usuario)))
        return True
    return False