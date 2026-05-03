from logica.repartidor_service import RepartidorService

repartidor_service = RepartidorService()


def manejar_post(path, body, responder):
    if path == "/repartidor/estado":
        id_usuario = body.get("id_usuario")
        estado = body.get("estado")
        if not id_usuario or not estado:
            responder(400, {"exito": False, "mensaje": "id_usuario y estado requeridos"})
            return True
        responder(200, repartidor_service.cambiar_estado(id_usuario, estado))
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/repartidores/disponibles":
        responder(200, repartidor_service.listar_disponibles())
        return True

    elif path == "/repartidores/limpios":
        responder(200, repartidor_service.listar_repartidores_limpios())
        return True

    elif path == "/repartidores/cercanos":
        lat = query.get("lat", [None])[0]
        lon = query.get("lon", [None])[0]
        if not lat or not lon:
            responder(400, {"exito": False, "mensaje": "lat y lon del restaurante requeridos"})
            return True
        responder(200, repartidor_service.listar_disponibles_cercanos(float(lat), float(lon)))
        return True

    return False