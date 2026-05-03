from datos.conexion import obtener_conexion
from modelo.restaurante import Restaurante


class RestauranteDAO:

    def guardar(self, restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Restaurante (nombre, cedula_juridica, direccion, tipo_comida, latitud, longitud, imagen, id_encargado)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    restaurante.nombre,
                    restaurante.cedula_juridica,
                    restaurante.direccion,
                    restaurante.tipo_comida,
                    restaurante.latitud,
                    restaurante.longitud,
                    restaurante.imagen,
                    restaurante.id_encargado
                )
                cursor.execute(sql, valores)
                conexion.commit()
                restaurante.set_id(cursor.lastrowid)
                return restaurante
            except Exception as e:
                print(f"Error al guardar restaurante: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def listar_todos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT id, nombre, cedula_juridica, direccion, tipo_comida, latitud, longitud, imagen FROM Restaurante")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar restaurantes: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula_juridica(self, cedula_juridica):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id FROM Restaurante WHERE cedula_juridica = %s", (cedula_juridica,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error al buscar restaurante: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Restaurante WHERE id = %s", (id_restaurante,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error al buscar restaurante por id: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()