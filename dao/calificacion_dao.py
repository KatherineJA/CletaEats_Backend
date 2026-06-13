from datos.conexion import obtener_conexion
import psycopg2.extras

class CalificacionDAO:

    def ya_califico(self, id_pedido, id_evaluador):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM calificacion WHERE id_pedido = %s AND id_evaluador = %s",
                    (id_pedido, id_evaluador)
                )
                fila = cursor.fetchone()
                return (fila[0] if fila else 0) > 0
            except Exception as e:
                print(f"Error al verificar calificación: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()
        return False

    def guardar(self, id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion=""):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_calificacion_guardar(%s,%s,%s,%s,%s,%s)",
                               (id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion))
                conexion.commit()
                return True
            except Exception as e:
                if "unique" in str(e).lower():
                    raise ValueError("Ya existe una calificación de este evaluador para este pedido")
                print(f"Error al guardar calificación: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def contar_malos_por_evaluado(self, id_evaluado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT fn_calificacion_contar_malos(%s)", (id_evaluado,))
                fila = cursor.fetchone()
                return fila[0] if fila else 0
            except Exception as e:
                print(f"Error al contar calificaciones MALO: {e}")
                return 0
            finally:
                cursor.close()
                conexion.close()

    def listar_por_pedido(self, id_pedido):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_calificacion_listar_por_pedido(%s)", (id_pedido,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar calificaciones: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_malos_por_repartidor(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_reporte_malos_por_repartidor()")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error en reporte M: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()