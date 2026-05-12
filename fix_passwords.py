import bcrypt
import mysql.connector
import os


conexion = mysql.connector.connect(
    host=os.environ.get("MYSQLHOST"),
    user=os.environ.get("MYSQLUSER"),
    password=os.environ.get("MYSQLPASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
    port=int(os.environ.get("MYSQLPORT", 3306))
)

password = "password123"
hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor = conexion.cursor()
cursor.execute("UPDATE Usuario SET contrasena = %s", (hash_pw,))
conexion.commit()
print(f"Actualizados {cursor.rowcount} usuarios con hash: {hash_pw}")
cursor.close()
conexion.close()