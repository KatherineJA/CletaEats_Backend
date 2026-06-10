from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import mimetypes
import re

from control import (
    auth_control,
    usuario_control,
    restaurante_control,
    encargado_control,
    repartidor_control,
    pedido_control,
    calificacion_control,
    reporte_control,
    combo_control,
)


class Router(BaseHTTPRequestHandler):

    def _responder(self, codigo, datos):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))

    def _leer_body(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            return self._leer_body_multipart(content_type)

        try:
            largo = int(self.headers.get("Content-Length", 0))
            if largo == 0:
                return {}
            body = self.rfile.read(largo)
            return json.loads(body.decode("utf-8"))
        except Exception:
            return {}

    def _leer_body_multipart(self, content_type):
        try:
            largo = int(self.headers.get("Content-Length", 0))
            if largo == 0:
                return {}
            payload = self.rfile.read(largo)
            boundary = self._extraer_boundary(content_type)
            if not boundary:
                return {}

            partes = payload.split(b"--" + boundary)
            body = {}
            for parte in partes:
                normalizado = parte.strip()
                if not normalizado or normalizado == b"--":
                    continue

                headers_blob, separador, contenido = normalizado.partition(b"\r\n\r\n")
                if not separador:
                    continue

                headers = self._parsear_headers_multipart(headers_blob)
                disposition = headers.get("content-disposition", "")
                nombre = self._extraer_parametro_disposition(disposition, "name")
                if not nombre:
                    continue

                contenido = contenido.rstrip(b"\r\n")
                filename = self._extraer_parametro_disposition(disposition, "filename")
                if filename:
                    valor = {
                        "filename": os.path.basename(filename),
                        "content_type": headers.get("content-type", "application/octet-stream"),
                        "data": contenido,
                    }
                else:
                    try:
                        valor = contenido.decode("utf-8")
                    except UnicodeDecodeError:
                        valor = contenido.decode("latin-1")

                if nombre in body:
                    if isinstance(body[nombre], list):
                        body[nombre].append(valor)
                    else:
                        body[nombre] = [body[nombre], valor]
                else:
                    body[nombre] = valor
            return body
        except Exception:
            return {}

    @staticmethod
    def _extraer_boundary(content_type):
        match = re.search(r"boundary=([^;]+)", content_type)
        if not match:
            return None
        boundary = match.group(1).strip().strip('"')
        return boundary.encode("utf-8")

    @staticmethod
    def _parsear_headers_multipart(headers_blob):
        headers = {}
        for linea in headers_blob.decode("latin-1").split("\r\n"):
            if ":" not in linea:
                continue
            clave, valor = linea.split(":", 1)
            headers[clave.strip().lower()] = valor.strip()
        return headers

    @staticmethod
    def _extraer_parametro_disposition(disposition, nombre):
        pattern = rf'{nombre}="([^"]*)"'
        match = re.search(pattern, disposition)
        return match.group(1) if match else None

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
    # POST (Evaluación explícita para evitar cortocircuitos erróneos)
    # ------------------------------------------------------------------
    def do_POST(self):
        try:
            body = self._leer_body()
            path = urlparse(self.path).path

            # Lista ordenada de todos los controladores POST disponibles
            controladores = [
                combo_control,
                auth_control,
                usuario_control,
                restaurante_control,
                encargado_control,
                repartidor_control,
                pedido_control,
                calificacion_control

            ]

            manejado = False
            for controlador in controladores:
                # Cada controlador debe retornar True únicamente si la ruta coincidió
                if controlador.manejar_post(path, body, self._responder):
                    manejado = True
                    break

            if not manejado:
                self._responder(404, {"exito": False, "mensaje": f"Ruta POST '{path}' no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": f"Error interno en Router POST: {str(e)}"})

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            query = parse_qs(parsed.query)

            if path.startswith("/fotos_perfil/") or path.startswith("/uploads/combos/"):
                ruta_archivo = path.lstrip("/")
                if os.path.isfile(ruta_archivo):
                    self.send_response(200)
                    content_type = mimetypes.guess_type(ruta_archivo)[0] or "application/octet-stream"
                    self.send_header("Content-Type", content_type)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    with open(ruta_archivo, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self._responder(404, {"exito": False, "mensaje": "Imagen no encontrada"})
                return

            # Lista ordenada de todos los controladores GET disponibles
            controladores = [
                combo_control,
                usuario_control,
                restaurante_control,
                encargado_control,
                repartidor_control,
                pedido_control,
                reporte_control

            ]

            manejado = False
            for controlador in controladores:
                if controlador.manejar_get(path, query, self._responder):
                    manejado = True
                    break

            if not manejado:
                self._responder(404, {"exito": False, "mensaje": f"Ruta GET '{path}' no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": f"Error interno en Router GET: {str(e)}"})

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")