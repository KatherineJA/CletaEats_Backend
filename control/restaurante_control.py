from logica.restaurante_service import RestauranteService

restaurante_service = RestauranteService()


def manejar_post(path, body, responder):
    if path == "/restaurante":
        campos = ["nombre", "cedula_juridica", "direccion", "tipo_comida"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, restaurante_service.registrar_restaurante(
            body["nombre"], body["cedula_juridica"], body["direccion"], body["tipo_comida"],
            body.get("latitud"), body.get("longitud"), body.get("id_encargado")
        ))
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/restaurantes":
        responder(200, restaurante_service.listar_restaurantes())
        return True

    elif path == "/restaurante/menu":
        id_res = query.get("id", [None])[0]
        if not id_res:
            responder(400, {"exito": False, "mensaje": "ID de restaurante requerido"})
            return True
        responder(200, restaurante_service.obtener_menu(id_res))
        return True

    return False