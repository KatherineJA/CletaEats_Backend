from datos.conexion import obtener_conexion
import psycopg2.extras

class EncargadoDAO:

    def guardar(self, id_usuario, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_encargado_guardar(%s,%s)", (id_usuario, id_restaurante))
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
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_encargado_buscar_por_id(%s)", (id_usuario,))
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
                cursor.execute("SELECT * FROM sp_encargado_buscar_restaurante(%s)", (id_usuario,))
                fila = cursor.fetchone()
                return fila[0] if fila else None
            except Exception as e:
                print(f"Error al buscar restaurante del encargado: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()