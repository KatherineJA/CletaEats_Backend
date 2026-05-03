from http.server import HTTPServer
from control.router import Router

if __name__ == "__main__":
    servidor = HTTPServer(("0.0.0.0", 5000), Router)
    print("Servidor CletaEats corriendo en http://localhost:5000")
    servidor.serve_forever()
