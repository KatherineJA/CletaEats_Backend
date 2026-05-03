from logica.pedido_service import PedidoService

pedido_service = PedidoService()


def manejar_post(path, body, responder):
    if path == "/pedido":
        campos = ["id_cliente", "id_restaurante", "lat_restaurante", "lon_restaurante",
                  "lat_destino", "lon_destino", "items"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, pedido_service.crear_pedido(
            body["id_cliente"], body["id_restaurante"],
            body["lat_restaurante"], body["lon_restaurante"],
            body["lat_destino"], body["lon_destino"],
            body["items"]
        ))
        return True

    elif path == "/pedido/estado":
        id_pedido = body.get("id_pedido")
        nuevo_estado = body.get("estado")
        if not id_pedido or not nuevo_estado:
            responder(400, {"exito": False, "mensaje": "id_pedido y estado requeridos"})
            return True
        responder(200, pedido_service.cambiar_estado(
            id_pedido, nuevo_estado, body.get("id_repartidor")
        ))
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/pedidos/disponibles":
        responder(200, pedido_service.pedidos_disponibles())
        return True

    elif path == "/pedidos/cliente":
        id_cliente = query.get("id", [None])[0]
        if not id_cliente:
            responder(400, {"exito": False, "mensaje": "ID de cliente requerido"})
            return True
        responder(200, pedido_service.historial_cliente(id_cliente))
        return True

    elif path == "/pedidos/repartidor":
        id_repartidor = query.get("id", [None])[0]
        if not id_repartidor:
            responder(400, {"exito": False, "mensaje": "ID de repartidor requerido"})
            return True
        responder(200, pedido_service.historial_repartidor(id_repartidor))
        return True

    elif path == "/pedido/detalle":
        id_pedido = query.get("id", [None])[0]
        if not id_pedido:
            responder(400, {"exito": False, "mensaje": "ID de pedido requerido"})
            return True
        responder(200, pedido_service.detalle_pedido(id_pedido))
        return True

    return False