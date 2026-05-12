from datos.conexion import obtener_conexion
from modelo.repartidor import Repartidor


class RepartidorDAO:

    def guardar(self, repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO Repartidor (id_usuario, numero_tarjeta, estado, kilometros_diarios) VALUES (%s, %s, %s, %s)"
                valores = (repartidor.id_usuario, repartidor.numero_tarjeta, repartidor.estado, repartidor.kilometros_diarios)
                cursor.execute(sql, valores)
                conexion.commit()
                return repartidor
            except Exception as e:
                print(f"Error al guardar repartidor: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id_usuario, numero_tarjeta, estado, kilometros_diarios FROM Repartidor WHERE id_usuario = %s", (id_usuario,))
                fila = cursor.fetchone()
                if fila:
                    r = Repartidor()
                    r.id_usuario, r.numero_tarjeta, r.estado, r.kilometros_diarios = fila
                    return r
                return None
            except Exception as e:
                print(f"Error al buscar repartidor: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_estado(self, id_usuario, estado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE Repartidor SET estado = %s WHERE id_usuario = %s", (estado, id_usuario))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar estado repartidor: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def listar_disponibles(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """
                    SELECT u.id, u.nombre, u.cedula, u.latitud, u.longitud, r.kilometros_diarios
                    FROM Usuario u
                    JOIN Repartidor r ON u.id = r.id_usuario
                    WHERE r.estado = 'DISPONIBLE'
                      AND (
                          SELECT COUNT(*) FROM Calificacion
                          WHERE id_evaluado = u.id AND tipo = 'MALO'
                      ) < 4
                """
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar repartidores disponibles: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_sin_calificaciones_malo(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """
                    SELECT u.id, u.cedula, u.nombre
                    FROM Usuario u
                    JOIN Repartidor r ON u.id = r.id_usuario
                    WHERE (
                        SELECT COUNT(*) FROM Calificacion
                        WHERE id_evaluado = u.id AND tipo = 'MALO'
                    ) = 0
                """
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar repartidores limpios: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()