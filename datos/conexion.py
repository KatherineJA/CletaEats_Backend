import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    try:
        return psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            dbname=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT", 5432))
        )
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None