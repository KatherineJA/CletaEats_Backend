from logica.pedido_service import PedidoService

pedido_service = PedidoService()


def manejar_post(path, body, responder):
    if path == "/calificacion":
        campos = ["id_pedido", "id_evaluador", "id_evaluado", "rol_evaluador", "tipo"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, pedido_service.calificar(
            body["id_pedido"], body["id_evaluador"], body["id_evaluado"],
            body["rol_evaluador"], body["tipo"], body.get("opinion", "")
        ))
        return True

    return False