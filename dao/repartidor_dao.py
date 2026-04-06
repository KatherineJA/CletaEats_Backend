from datos.conexion import obtener_conexion

class RepartidorDAO:
    def guardar(self, repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO repartidor 
                         (usuario_id, cedula, nombre, correo, direccion, telefono, tarjeta) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valores = (repartidor.usuario_id, repartidor.cedula, repartidor.nombre,
                           repartidor.correo, repartidor.direccion, repartidor.telefono, repartidor.tarjeta)
                cursor.execute(sql, valores)
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al guardar repartidor: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula(self, cedula):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "SELECT id FROM repartidor WHERE cedula = %s"
                cursor.execute(sql, (cedula,))
                return cursor.fetchone() is not None
            finally:
                cursor.close()
                conexion.close()
        return False

    def obtener_disponibles_sin_faltas(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = "SELECT * FROM repartidor WHERE amonestaciones = 0"
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                cursor.close()
                conexion.close()
        return []