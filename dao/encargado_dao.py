from datos.conexion import obtener_conexion


class EncargadoDAO:

    def guardar(self, id_usuario, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""INSERT INTO EncargadoRestaurante (id_usuario, id_restaurante)
                                  VALUES (%s, %s)""", (id_usuario, id_restaurante))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al guardar encargado: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""SELECT e.id_usuario, e.id_restaurante, r.nombre AS nombre_restaurante
                                  FROM EncargadoRestaurante e
                                  JOIN Restaurante r ON e.id_restaurante = r.id
                                  WHERE e.id_usuario = %s""", (id_usuario,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error al buscar encargado: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_restaurante_de_encargado(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""SELECT id_restaurante FROM EncargadoRestaurante
                                  WHERE id_usuario = %s""", (id_usuario,))
                fila = cursor.fetchone()
                return fila[0] if fila else None
            except Exception as e:
                print(f"Error al buscar restaurante del encargado: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()