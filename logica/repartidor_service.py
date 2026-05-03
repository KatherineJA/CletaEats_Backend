from dao.repartidor_dao import RepartidorDAO


class RepartidorService:

    def __init__(self):
        self.repartidor_dao = RepartidorDAO()

    def listar_disponibles(self):
        repartidores = self.repartidor_dao.listar_disponibles()
        return {"exito": True, "datos": repartidores}

    def listar_repartidores_limpios(self):
        """Reporte G: repartidores con cero calificaciones MALO."""
        repartidores = self.repartidor_dao.listar_sin_calificaciones_malo()
        return {"exito": True, "datos": repartidores}

    def cambiar_estado(self, id_usuario, estado):
        estados_validos = ["DISPONIBLE", "OCUPADO", "SUSPENDIDO"]
        if estado not in estados_validos:
            return {"exito": False, "mensaje": f"Estado inválido. Opciones: {estados_validos}"}
        ok = self.repartidor_dao.actualizar_estado(id_usuario, estado)
        return {"exito": ok, "mensaje": "Estado actualizado" if ok else "Error al actualizar estado"}