from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from control import (
    auth_control,
    restaurante_control,
    repartidor_control,
    pedido_control,
    calificacion_control,
    reporte_control,
)


class Router(BaseHTTPRequestHandler):

    def _responder(self, codigo, datos):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))

    def _leer_body(self):
        try:
            largo = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(largo)
            return json.loads(body.decode("utf-8"))
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ------------------------------------------------------------------
    # POST — delega en orden hasta que algún control lo maneje
    # ------------------------------------------------------------------
    def do_POST(self):
        try:
            body = self._leer_body()
            path = urlparse(self.path).path

            manejado = (
                auth_control.manejar_post(path, body, self._responder) or
                restaurante_control.manejar_post(path, body, self._responder) or
                repartidor_control.manejar_post(path, body, self._responder) or
                pedido_control.manejar_post(path, body, self._responder) or
                calificacion_control.manejar_post(path, body, self._responder)
            )

            if not manejado:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    # ------------------------------------------------------------------
    # GET — delega en orden hasta que algún control lo maneje
    # ------------------------------------------------------------------
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            manejado = (
                restaurante_control.manejar_get(path, query, self._responder) or
                repartidor_control.manejar_get(path, query, self._responder) or
                pedido_control.manejar_get(path, query, self._responder) or
                reporte_control.manejar_get(path, query, self._responder)
            )

            if not manejado:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")