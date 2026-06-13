import bcrypt
import psycopg2
import os


conexion = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    dbname=os.environ.get("DB_NAME"),
    port=int(os.environ.get("DB_PORT", 5432))
)

password = "password123"
hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor = conexion.cursor()
cursor.execute("UPDATE Usuario SET contrasena = %s", (hash_pw,))
conexion.commit()
print(f"Actualizados {cursor.rowcount} usuarios con hash: {hash_pw}")
cursor.close()
conexion.close()