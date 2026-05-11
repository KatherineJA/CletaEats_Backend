import bcrypt
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cletaeats"
)

password = "password123"
hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cursor = conexion.cursor()
cursor.execute("UPDATE Usuario SET contrasena = %s", (hash_pw,))
conexion.commit()
print(f"Actualizados {cursor.rowcount} usuarios con hash: {hash_pw}")
cursor.close()
conexion.close()