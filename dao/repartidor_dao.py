from datos.conexion import obtener_conexion
from modelo.repartidor import Repartidor


class RepartidorDAO:

    def guardar(self, repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.callproc('sp_repartidor_guardar', (
                    repartidor.id_usuario,
                    repartidor.numero_tarjeta,
                    repartidor.estado,
                    repartidor.kilometros_diarios
                ))
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
                cursor.callproc('sp_repartidor_buscar_por_id', (id_usuario,))
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    if fila:
                        r = Repartidor()
                        r.id_usuario, r.numero_tarjeta, r.estado, r.kilometros_diarios, \
                        _, _, _ = fila  # nombre, latitud, longitud los ignora (son de Usuario)
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
                cursor.callproc('sp_repartidor_actualizar_estado', (id_usuario, estado))
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
                cursor.callproc('sp_repartidor_listar_disponibles_filtrado')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
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
                cursor.callproc('sp_repartidor_listar_sin_malos')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar repartidores limpios: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()