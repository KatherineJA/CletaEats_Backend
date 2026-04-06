from datos.conexion import obtener_conexion

class ComboDAO:
    def guardar(self, restaurante_id, numero, precio):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO combo (restaurante_id, numero, nombre, precio) VALUES (%s, %s, %s, %s)"
                valores = (restaurante_id, numero, f"Combo No. {numero}", precio)
                cursor.execute(sql, valores)
                conexion.commit()
            except Exception as e:
                print(f"Error al guardar combo automático: {e}")
            finally:
                cursor.close()
                conexion.close()

    def listar_por_restaurante(self, restaurante_id):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                # Los combos van del 1 al 9
                sql = "SELECT * FROM combo WHERE restaurante_id = %s ORDER BY numero"
                cursor.execute(sql, (restaurante_id,))
                return cursor.fetchall()
            finally:
                cursor.close()
                conexion.close()
        return []