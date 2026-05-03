from dao.reporte_dao import ReporteDAO


class ReporteService:

    def __init__(self):
        self.reporte_dao = ReporteDAO()

    def reporte_clientes_regitrados(self): return {"exito": True, "datos": self.reporte_dao.clientes_registrados()}
    def reporte_restaurantes_registrados(self): return {"exito": True, "datos": self.reporte_dao.restaurantes_registrados()}
    def reporte_repartidores_registrados(self): return {"exito": True, "datos": self.reporte_dao.repartidores_registrados()}
    def reporte_pedidos_registrados(self): return {"exito": True, "datos": self.reporte_dao.pedidos_registrados()}
    def reporte_clientes_activos(self): return {"exito": True, "datos": self.reporte_dao.clientes_activos()}
    def reporte_clientes_suspendidos(self): return {"exito": True, "datos": self.reporte_dao.clientes_suspendidos()}
    def reporte_repartidores_sin_malos(self): return {"exito": True, "datos": self.reporte_dao.repartidores_sin_malos()}
    def reporte_restaurantes_listado(self): return {"exito": True, "datos": self.reporte_dao.restaurantes_listado()}
    def reporte_restaurante_mas_pedidos(self): return {"exito": True, "datos": self.reporte_dao.restaurante_mas_pedidos()}
    def reporte_monto_por_restaurante(self): return {"exito": True, "datos": self.reporte_dao.monto_por_restaurante()}
    def reporte_monto_total_global(self): return {"exito": True, "datos": self.reporte_dao.monto_total_global()}
    def reporte_restaurante_menos_pedidos(self): return {"exito": True, "datos": self.reporte_dao.restaurante_menos_pedidos()}
    def reporte_malos_por_repartidor(self): return {"exito": True, "datos": self.reporte_dao.malos_por_repartidor()}
    def reporte_pedidos_por_cliente(self): return {"exito": True, "datos": self.reporte_dao.pedidos_por_cliente()}
    def reporte_cliente_mas_pedidos(self): return {"exito": True, "datos": self.reporte_dao.cliente_mas_pedidos()}
    def reporte_hora_pico(self): return {"exito": True, "datos": self.reporte_dao.hora_pico()}