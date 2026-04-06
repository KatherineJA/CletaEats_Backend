from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from logica.auth_service import AuthService
from logica.restaurante_service import RestauranteService
from logica.repartidor_service import RepartidorService

# Instancias de los servicios
auth_service = AuthService()
restaurante_service = RestauranteService()
repartidor_service = RepartidorService()

class Control(BaseHTTPRequestHandler):

    def _responder(self, codigo, datos):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        respuesta_json = json.dumps(datos, default=str)
        self.wfile.write(respuesta_json.encode("utf-8"))

    def _leer_body(self):
        try:
            largo = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(largo)
            return json.loads(body.decode("utf-8"))
        except:
            return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            body = self._leer_body()

            if self.path == "/login":
                correo = body.get("correo")
                password = body.get("password")
                if not correo or not password:
                    self._responder(400, {"exito": False, "mensaje": "Correo y contraseña requeridos"})
                    return
                resultado = auth_service.login(correo, password)
                self._responder(200, resultado)

            elif self.path == "/registro":
                campos = ["correo", "password", "cedula", "nombre", "direccion", "tarjeta", "telefono"]
                if not all(body.get(c) for c in campos):
                    self._responder(400, {"exito": False, "mensaje": "Todos los campos son requeridos"})
                    return
                resultado = auth_service.registrar_cliente(
                    body["correo"], body["password"], body["cedula"],
                    body["nombre"], body["direccion"], body["tarjeta"], body["telefono"]
                )
                self._responder(200, resultado)

            elif self.path == "/restaurante":
                campos_res = ["cedula_juridica", "nombre", "direccion", "tipo_comida"]
                if not all(body.get(c) for c in campos_res):
                    self._responder(400, {"exito": False, "mensaje": "Todos los campos son requeridos"})
                    return
                resultado = restaurante_service.registrar_restaurante(
                    body["cedula_juridica"], body["nombre"], body["direccion"], body["tipo_comida"]
                )
                self._responder(200, resultado)

            elif self.path == "/repartidor":
                campos_rep = ["cedula", "nombre", "correo", "direccion", "telefono", "tarjeta"]
                if not all(body.get(c) for c in campos_rep):
                    self._responder(400, {"exito": False, "mensaje": "Datos del repartidor incompletos"})
                    return
                # Asegúrate que este nombre coincida en RepartidorService
                resultado = repartidor_service.registrar_repartidor(body)
                self._responder(200, resultado)

            else:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})

        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    def do_GET(self):
        try:
            if self.path == "/restaurantes":
                resultado = restaurante_service.listar_restaurantes()
                self._responder(200, resultado)

            elif self.path == "/repartidores/limpios":
                # Reporte G: Cero amonestaciones
                resultado = repartidor_service.listar_repartidores_limpios()
                self._responder(200, resultado)

            elif self.path.startswith("/restaurante/menu"):
                from urllib.parse import urlparse, parse_qs
                query = parse_qs(urlparse(self.path).query)
                res_id = query.get('id', [None])[0]

                if res_id:
                    resultado = restaurante_service.obtener_menu(res_id)
                    self._responder(200, resultado)
                else:
                    self._responder(400, {"exito": False, "mensaje": "ID de restaurante requerido"})

            else:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})
        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    # Evita el error "Shadows built-in name 'format'" cambiando el nombre de los argumentos
    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")

if __name__ == "__main__":
    servidor = HTTPServer(("0.0.0.0", 5000), Control)
    print("Servidor CletaEats corriendo en puerto 5000")
    servidor.serve_forever()