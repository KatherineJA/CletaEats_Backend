import math
from dao.pedido_dao import PedidoDAO
from dao.calificacion_dao import CalificacionDAO
from dao.cliente_dao import ClienteDAO
from dao.repartidor_dao import RepartidorDAO


class PedidoService:

    def __init__(self):
        self.pedido_dao = PedidoDAO()
        self.calificacion_dao = CalificacionDAO()
        self.cliente_dao = ClienteDAO()
        self.repartidor_dao = RepartidorDAO()

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
                     items):
        cliente = self.cliente_dao.buscar_por_id(id_cliente)
        if not cliente or not cliente.esta_activo():
            return {"exito": False, "mensaje": "El cliente está suspendido y no puede realizar pedidos."}

        subtotal = sum(
            (item['precio_unitario'] + item.get('extras_costo', 0)) * item['cantidad']
            for item in items
        )

        distancia_km = self.calcular_distancia_km(lat_restaurante, lon_restaurante, lat_destino, lon_destino)
        porcentaje = self.calcular_porcentaje_envio(distancia_km)
        costo_envio = round(subtotal * porcentaje, 2)
        iva = round((subtotal + costo_envio) * 0.13, 2)
        total = round(subtotal + costo_envio + iva, 2)

        id_pedido = self.pedido_dao.guardar(
            id_cliente, id_restaurante, lat_destino, lon_destino, distancia_km, costo_envio
        )
        if not id_pedido:
            return {"exito": False, "mensaje": "Error al guardar el pedido"}

        for item in items:
            id_detalle = self.pedido_dao.guardar_detalle(id_pedido, item['id_combo'], item['cantidad'])
            if id_detalle:
                for id_valor in item.get('valores_opcion', []):
                    self.pedido_dao.guardar_preferencia(id_detalle, id_valor)

        return {
            "exito": True,
            "id_pedido": id_pedido,
            "resumen": {
                "subtotal": subtotal,
                "distancia_km": round(distancia_km, 2),
                "porcentaje_envio": f"{int(porcentaje * 100)}%",
                "costo_envio": costo_envio,
                "iva": iva,
                "total": total
            }
        }

    def cambiar_estado(self, id_pedido, nuevo_estado, id_solicitante, rol_solicitante, id_repartidor=None):
        estados_validos = ["EN_PREPARACION", "EN_CAMINO", "ENTREGADO", "CANCELADO"]
        if nuevo_estado not in estados_validos:
            return {"exito": False, "mensaje": f"Estado inválido. Opciones: {estados_validos}"}

        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido:
            return {"exito": False, "mensaje": "Pedido no encontrado"}

        if nuevo_estado == "CANCELADO":
            if rol_solicitante != "CLIENTE" or pedido["id_cliente"] != id_solicitante:
                return {"exito": False, "mensaje": "Solo el cliente dueño del pedido puede cancelarlo"}
            if pedido["estado"] not in ("EN_PREPARACION", "EN_CAMINO"):
                return {"exito": False, "mensaje": "Solo se puede cancelar un pedido activo"}

        if nuevo_estado == "EN_CAMINO" and id_repartidor:
            pedidos_activos = self.pedido_dao.contar_pedidos_activos_repartidor(id_repartidor)
            if pedidos_activos > 0:
                return {"exito": False, "mensaje": "Ya tenés un pedido activo. Debés entregarlo antes de aceptar otro."}

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

    def calificar(self, id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion=""):
        if tipo not in ("BUENO", "REGULAR", "MALO"):
            return {"exito": False, "mensaje": "Tipo inválido. Opciones: BUENO, REGULAR, MALO"}

        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido or pedido["estado"] != "ENTREGADO":
            return {"exito": False, "mensaje": "Solo se puede calificar pedidos entregados"}

        try:
            self.calificacion_dao.guardar(id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion)
        except ValueError as e:
            return {"exito": False, "mensaje": str(e)}

        if tipo == "MALO":
            rol_evaluado = "REPARTIDOR" if rol_evaluador == "CLIENTE" else "CLIENTE"
            total_malos = self.calificacion_dao.contar_malos_por_evaluado(id_evaluado)
            if total_malos >= 4:
                if rol_evaluado == "REPARTIDOR":
                    self.repartidor_dao.actualizar_estado(id_evaluado, "SUSPENDIDO")
                else:
                    self.cliente_dao.actualizar_estado(id_evaluado, "SUSPENDIDO")

        return {"exito": True, "mensaje": "Calificación guardada"}

    def historial_cliente(self, id_cliente):
        return {"exito": True, "datos": self.pedido_dao.listar_por_cliente(id_cliente)}

    def historial_repartidor(self, id_repartidor):
        return {"exito": True, "datos": self.pedido_dao.listar_por_repartidor(id_repartidor)}

    def pedidos_disponibles(self):
        return {"exito": True, "datos": self.pedido_dao.listar_disponibles()}

    def detalle_pedido(self, id_pedido):
        pedido = self.pedido_dao.buscar_por_id(id_pedido)
        if not pedido:
            return {"exito": False, "mensaje": "Pedido no encontrado"}
        pedido["items"] = self.pedido_dao.listar_detalles(id_pedido)
        return {"exito": True, "datos": pedido}