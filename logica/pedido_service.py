import math
from dao.pedido_dao import PedidoDAO
from dao.calificacion_dao import CalificacionDAO
from dao.cliente_dao import ClienteDAO
from dao.repartidor_dao import RepartidorDAO
from dao.usuario_dao import UsuarioDAO


class PedidoService:

    def __init__(self):
        self.pedido_dao       = PedidoDAO()
        self.calificacion_dao = CalificacionDAO()
        self.cliente_dao      = ClienteDAO()
        self.repartidor_dao   = RepartidorDAO()
        self.usuario_dao      = UsuarioDAO()

    def calcular_distancia_km(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))

    def calcular_porcentaje_envio(self, distancia_km):
        if distancia_km <= 3:
            return 0.10
        elif distancia_km <= 6:
            return 0.20
        elif distancia_km <= 10:
            return 0.30
        else:
            return 0.50

    def crear_pedido(self, id_cliente, id_restaurante,
                     lat_restaurante, lon_restaurante,
                     lat_destino, lon_destino,
                     items,
                     metodo_pago="EFECTIVO",
                     numero_tarjeta=None):
        cliente = self.cliente_dao.buscar_por_id(id_cliente)
        if not cliente or not cliente.esta_activo():
            return {"exito": False,
                    "mensaje": "El cliente esta suspendido y no puede realizar pedidos."}

        if metodo_pago == "TARJETA":
            tarjeta_a_usar = numero_tarjeta or cliente.numero_tarjeta
            if not tarjeta_a_usar:
                return {"exito": False,
                        "mensaje": "No hay tarjeta disponible para el pago."}
            # Si el cliente quiso guardar la tarjeta nueva, actualizarla
            if numero_tarjeta and numero_tarjeta != cliente.numero_tarjeta:
                self.usuario_dao.actualizar_tarjeta_cliente(id_cliente, numero_tarjeta)

        subtotal = sum(
            (item["precio_unitario"] + item.get("extras_costo", 0)) * item["cantidad"]
            for item in items
        )

        distancia_km  = self.calcular_distancia_km(
            lat_restaurante, lon_restaurante, lat_destino, lon_destino
        )
        porcentaje    = self.calcular_porcentaje_envio(distancia_km)
        costo_envio   = round(subtotal * porcentaje, 2)
        iva           = round((subtotal + costo_envio) * 0.13, 2)
        total         = round(subtotal + costo_envio + iva, 2)

        id_pedido = self.pedido_dao.guardar(
            id_cliente, id_restaurante,
            lat_destino, lon_destino,
            distancia_km, costo_envio
        )
        if not id_pedido:
            return {"exito": False, "mensaje": "Error al guardar el pedido"}

        for item in items:
            id_detalle = self.pedido_dao.guardar_detalle(
                id_pedido, item["id_combo"], item["cantidad"]
            )
            if id_detalle:
                for id_valor in item.get("valores_opcion", []):
                    self.pedido_dao.guardar_preferencia(id_detalle, id_valor)

        return {
            "exito":     True,
            "id_pedido": id_pedido,
            "resumen": {
                "subtotal":          subtotal,
                "distancia_km":      round(distancia_km, 2),
                "porcentaje_envio":  f"{int(porcentaje * 100)}%",
                "costo_envio":       costo_envio,
                "iva":               iva,
                "total":             total
            }
        }

    def cambiar_estado(self, id_pedido, nuevo_estado,
                       id_solicitante, rol_solicitante,
                       id_repartidor=None):
        estados_validos = ["EN_PREPARACION", "EN_CAMINO", "ENTREGADO", "CANCELADO"]
        if nuevo_estado not in estados_validos:
            return {"exito": False,
                    "mensaje": f"Estado invalido. Opciones: {estados_validos}"}

        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido:
            return {"exito": False, "mensaje": "Pedido no encontrado"}

        if nuevo_estado == "CANCELADO":
            if rol_solicitante == "CLIENTE":
                if pedido["id_cliente"] != id_solicitante:
                    return {"exito": False,
                            "mensaje": "Solo el cliente dueno del pedido puede cancelarlo"}
                if pedido["estado"] not in ("EN_PREPARACION", "EN_CAMINO"):
                    return {"exito": False,
                            "mensaje": "Solo se puede cancelar un pedido activo"}
            elif rol_solicitante == "REPARTIDOR":
                if pedido["id_repartidor"] != id_solicitante:
                    return {"exito": False,
                            "mensaje": "Solo el repartidor asignado puede cancelar el pedido"}
                if pedido["estado"] != "EN_CAMINO":
                    return {"exito": False,
                            "mensaje": "Solo podes cancelar un pedido que estas entregando"}
            else:
                return {"exito": False,
                        "mensaje": "No tenes permiso para cancelar este pedido"}

        ok = self.pedido_dao.actualizar_estado(id_pedido, nuevo_estado, id_repartidor)
        if not ok:
            return {"exito": False, "mensaje": "Error al actualizar el pedido"}

        if nuevo_estado == "EN_CAMINO" and id_repartidor:
            self.repartidor_dao.actualizar_estado(id_repartidor, "OCUPADO")
        elif nuevo_estado == "ENTREGADO":
            if pedido.get("id_repartidor"):
                self.repartidor_dao.actualizar_estado(pedido["id_repartidor"], "DISPONIBLE")
        elif nuevo_estado == "CANCELADO":
            if pedido.get("id_repartidor"):
                self.repartidor_dao.actualizar_estado(pedido["id_repartidor"], "DISPONIBLE")

        return {"exito": True, "mensaje": f"Pedido actualizado a {nuevo_estado}"}

    def calificar(self, id_pedido, id_evaluador, id_evaluado,
                  rol_evaluador, tipo, opinion=""):
        if tipo not in ("BUENO", "REGULAR", "MALO"):
            return {"exito": False,
                    "mensaje": "Tipo invalido. Opciones: BUENO, REGULAR, MALO"}

        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido:
            return {"exito": False, "mensaje": "Pedido no encontrado"}

        if pedido["estado"] != "ENTREGADO":
            return {"exito": False,
                    "mensaje": "Solo se puede calificar un pedido entregado"}

        ya_califico = self.calificacion_dao.ya_califico(id_pedido, id_evaluador)
        if ya_califico:
            return {"exito": False, "mensaje": "Ya calificaste este pedido"}

        ok = self.calificacion_dao.guardar(
            id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion
        )
        return {"exito": ok, "mensaje": "Calificacion guardada" if ok else "Error al guardar calificacion"}

    def historial_cliente(self, id_cliente):
        datos = self.pedido_dao.listar_por_cliente(id_cliente)
        return {"exito": True, "datos": datos}

    def historial_repartidor(self, id_repartidor):
        datos = self.pedido_dao.listar_por_repartidor(id_repartidor)
        return {"exito": True, "datos": datos}

    def pedidos_disponibles(self):
        datos = self.pedido_dao.listar_disponibles()
        return {"exito": True, "datos": datos}

    def detalle_pedido(self, id_pedido):
        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido:
            return {"exito": False, "mensaje": "Pedido no encontrado"}
        return {"exito": True, "datos": pedido}
