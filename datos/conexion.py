import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    print(f"Conectando a: {os.environ.get('DB_HOST')} / {os.environ.get('DB_NAME')}")
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            dbname=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT", 5432)),
            sslmode="require"
        )
        print("CONEXION EXITOSA")
        return conn
    except Exception as e:
        print("ERROR POSTGRES:", repr(e))
        return None