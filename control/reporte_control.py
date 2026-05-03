from logica.reporte_service import ReporteService

reporte_service = ReporteService()

_REPORTES = {
    "/reporte/a": reporte_service.reporte_a,
    "/reporte/b": reporte_service.reporte_b,
    "/reporte/c": reporte_service.reporte_c,
    "/reporte/d": reporte_service.reporte_d,
    "/reporte/e": reporte_service.reporte_e,
    "/reporte/f": reporte_service.reporte_f,
    "/reporte/g": reporte_service.reporte_g,
    "/reporte/h": reporte_service.reporte_h,
    "/reporte/i": reporte_service.reporte_i,
    "/reporte/j": reporte_service.reporte_j,
    "/reporte/k": reporte_service.reporte_k,
    "/reporte/l": reporte_service.reporte_l,
    "/reporte/m": reporte_service.reporte_m,
    "/reporte/n": reporte_service.reporte_n,
    "/reporte/o": reporte_service.reporte_o,
    "/reporte/p": reporte_service.reporte_p,
}


def manejar_get(path, query, responder):
    if path in _REPORTES:
        responder(200, _REPORTES[path]())
        return True
    return False