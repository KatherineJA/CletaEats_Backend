from http.server import HTTPServer
from control.router import Router
import os

PORT = int(os.environ.get("PORT", 5000))  # Railway inyecta PORT automáticamente

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Router)
    print(f"Servidor CletaEats corriendo en puerto {PORT}")
    server.serve_forever()