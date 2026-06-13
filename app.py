from http.server import HTTPServer
from control.router import Router
import os

PORT = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    try:
        os.makedirs("fotos_perfil", exist_ok=True)
        os.makedirs(os.path.join("uploads", "combos"), exist_ok=True)
    except Exception:
        pass
    server = HTTPServer(("0.0.0.0", PORT), Router)
    print(f"Servidor CletaEats corriendo en puerto {PORT}")
    server.serve_forever()