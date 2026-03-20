from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from logica.auth_service import AuthService
from logica.restaurante_service import RestauranteService

auth_service = AuthService()
restaurante_service = RestauranteService()

class Control(BaseHTTPRequestHandler):

    def _responder(self, codigo, datos):
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(datos).encode("utf-8"))

    def _leer_body(self):
        largo = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(largo)
        return json.loads(body.decode("utf-8"))

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
                correo = body.get("correo")
                password = body.get("password")
                cedula = body.get("cedula")
                nombre = body.get("nombre")
                direccion = body.get("direccion")
                tarjeta = body.get("tarjeta")
                telefono = body.get("telefono")
                if not all([correo, password, cedula, nombre, direccion, tarjeta, telefono]):
                    self._responder(400, {"exito": False, "mensaje": "Todos los campos son requeridos"})
                    return
                resultado = auth_service.registrar_cliente(correo, password, cedula, nombre, direccion, tarjeta, telefono)
                self._responder(200, resultado)

            elif self.path == "/restaurante":
                cedula_juridica = body.get("cedula_juridica")
                nombre = body.get("nombre")
                direccion = body.get("direccion")
                tipo_comida = body.get("tipo_comida")
                if not all([cedula_juridica, nombre, direccion, tipo_comida]):
                    self._responder(400, {"exito": False, "mensaje": "Todos los campos son requeridos"})
                    return
                resultado = restaurante_service.registrar_restaurante(cedula_juridica, nombre, direccion, tipo_comida)
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
            else:
                self._responder(404, {"exito": False, "mensaje": "Ruta no encontrada"})
        except Exception as e:
            self._responder(500, {"exito": False, "mensaje": str(e)})

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

if __name__ == "__main__":
    servidor = HTTPServer(("0.0.0.0", 5000), Control)
    print("Servidor CletaEats corriendo en puerto 5000")
    servidor.serve_forever()