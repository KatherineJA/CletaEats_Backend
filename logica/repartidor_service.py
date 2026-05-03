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

    def listar_disponibles_cercanos(self, lat_restaurante, lon_restaurante):
        """Repartidores disponibles ordenados por cercanía al restaurante (Haversine)."""
        import math

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            return R * 2 * math.asin(math.sqrt(a))

        repartidores = self.repartidor_dao.listar_disponibles()
        for r in repartidores:
            if r.get("latitud") and r.get("longitud"):
                r["distancia_km"] = round(
                    haversine(lat_restaurante, lon_restaurante, r["latitud"], r["longitud"]), 2
                )
            else:
                r["distancia_km"] = 9999

        repartidores.sort(key=lambda r: r["distancia_km"])
        return {"exito": True, "datos": repartidores}