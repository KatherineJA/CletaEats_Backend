from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

from control import (
    auth_control,
    usuario_control,
    restaurante_control,
    encargado_control,
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

    # ------------------------------------------------------------------
    # OPTIONS
    # ------------------------------------------------------------------
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ------------------------------------------------------------------
    # POST
    # ------------------------------------------------------------------
    def do_POST(self):
        try:
            body = self._leer_body()
            path = urlparse(self.path).path

            manejado = (
                auth_control.manejar_post(path, body, self._responder) or
                usuario_control.manejar_post(path, body, self._responder) or
                restaurante_control.manejar_post(path, body, self._responder) or
                encargado_control.manejar_post(path, body, self._responder) or
                repartidor_control.manejar_post(path, body, self._responder) or
                pedido_control.manejar_post(path, body, self._responder) or
                calificacion_control.manejar_post(path, body, self._responder)
            )

            if not manejado:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path.startswith("/fotos_perfil/"):
                ruta_archivo = path.lstrip("/")
                if os.path.isfile(ruta_archivo):
                    self.send_response(200)
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(ruta_archivo, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self._responder(404, {"exito": False, "mensaje": "Imagen no encontrada"})
                return

            manejado = (
                usuario_control.manejar_get(path, query, self._responder) or
                restaurante_control.manejar_get(path, query, self._responder) or
                encargado_control.manejar_get(path, query, self._responder) or
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