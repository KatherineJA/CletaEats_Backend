from logica.reporte_service import ReporteService

reporte_service = ReporteService()

_REPORTES = {
    "/reporte/clientes-registrados": reporte_service.reporte_clientes_regitrados,
    "/reporte/restaurantes-registrados": reporte_service.reporte_restaurantes_registrados,
    "/reporte/repartidores-registrados": reporte_service.reporte_repartidores_registrados,
    "/reporte/pedidos-registrados": reporte_service.reporte_pedidos_registrados,
    "/reporte/clientes-activos": reporte_service.reporte_clientes_activos,
    "/reporte/clientes-suspendidos": reporte_service.reporte_clientes_suspendidos,
    "/reporte/repartidores-buenos": reporte_service.reporte_repartidores_sin_malos,
    "/reporte/listado-restaurantes": reporte_service.reporte_restaurantes_listado,
    "/reporte/restaurantes-con-mas-pedidos": reporte_service.reporte_restaurante_mas_pedidos,
    "/reporte/ganancias-por-restaurante": reporte_service.reporte_monto_por_restaurante,
    "/reporte/monto-global-total": reporte_service.reporte_monto_total_global,
    "/reporte/restaurante-con-menos-pedidos": reporte_service.reporte_restaurante_menos_pedidos,
    "/reporte/repartidores-malos": reporte_service.reporte_malos_por_repartidor,
    "/reporte/pedidos-por-cliente": reporte_service.reporte_pedidos_por_cliente,
    "/reporte/cliente-con-mas-pedidos": reporte_service.reporte_cliente_mas_pedidos,
    "/reporte/hora-pico": reporte_service.reporte_hora_pico,
}


def manejar_get(path, query, responder):
    if path in _REPORTES:
        responder(200, _REPORTES[path]())
        return True
    return False