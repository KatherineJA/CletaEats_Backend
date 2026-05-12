import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # carga el .env

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host=os.environ.get("MYSQLHOST"),
            user=os.environ.get("MYSQLUSER"),
            password=os.environ.get("MYSQLPASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
            port=int(os.environ.get("MYSQLPORT", 3306))
        )
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None