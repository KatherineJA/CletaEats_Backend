from dao.reporte_dao import ReporteDAO


class ReporteService:

    def __init__(self):
        self.reporte_dao = ReporteDAO()

    def reporte_a(self): return {"exito": True, "datos": self.reporte_dao.clientes_registrados()}
    def reporte_b(self): return {"exito": True, "datos": self.reporte_dao.restaurantes_registrados()}
    def reporte_c(self): return {"exito": True, "datos": self.reporte_dao.repartidores_registrados()}
    def reporte_d(self): return {"exito": True, "datos": self.reporte_dao.pedidos_registrados()}
    def reporte_e(self): return {"exito": True, "datos": self.reporte_dao.clientes_activos()}
    def reporte_f(self): return {"exito": True, "datos": self.reporte_dao.clientes_suspendidos()}
    def reporte_g(self): return {"exito": True, "datos": self.reporte_dao.repartidores_sin_malos()}
    def reporte_h(self): return {"exito": True, "datos": self.reporte_dao.restaurantes_listado()}
    def reporte_i(self): return {"exito": True, "datos": self.reporte_dao.restaurante_mas_pedidos()}
    def reporte_j(self): return {"exito": True, "datos": self.reporte_dao.monto_por_restaurante()}
    def reporte_k(self): return {"exito": True, "datos": self.reporte_dao.monto_total_global()}
    def reporte_l(self): return {"exito": True, "datos": self.reporte_dao.restaurante_menos_pedidos()}
    def reporte_m(self): return {"exito": True, "datos": self.reporte_dao.malos_por_repartidor()}
    def reporte_n(self): return {"exito": True, "datos": self.reporte_dao.pedidos_por_cliente()}
    def reporte_o(self): return {"exito": True, "datos": self.reporte_dao.cliente_mas_pedidos()}
    def reporte_p(self): return {"exito": True, "datos": self.reporte_dao.hora_pico()}