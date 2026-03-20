from datos.conexion import obtener_conexion
from modelo.restaurante import Restaurante

class RestauranteDAO:

    def guardar(self, restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO restaurante 
                         (cedula_juridica, nombre, direccion, tipo_comida) 
                         VALUES (%s, %s, %s, %s)"""
                valores = (
                    restaurante.get_cedula_juridica(),
                    restaurante.get_nombre(),
                    restaurante.direccion,
                    restaurante.get_tipo_comida()
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
                cursor = conexion.cursor()
                sql = "SELECT id, cedula_juridica, nombre, direccion, tipo_comida FROM restaurante"
                cursor.execute(sql)
                filas = cursor.fetchall()
                restaurantes = []
                for fila in filas:
                    r = Restaurante()
                    r.set_id(fila[0])
                    r.set_cedula_juridica(fila[1])
                    r.set_nombre(fila[2])
                    r.direccion = fila[3]
                    r.set_tipo_comida(fila[4])
                    restaurantes.append(r)
                return restaurantes
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
                sql = "SELECT id FROM restaurante WHERE cedula_juridica = %s"
                cursor.execute(sql, (cedula_juridica,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error al buscar restaurante: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()