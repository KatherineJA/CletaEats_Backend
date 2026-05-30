from datos.conexion import obtener_conexion


class CalificacionDAO:

    def guardar(self, id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion=""):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.callproc('sp_calificacion_guardar',
                                (id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion))
                conexion.commit()
                return True
            except Exception as e:
                if "Duplicate entry" in str(e):
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
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_calificacion_listar_por_pedido', (id_pedido,))
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
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
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_calificacion_reporte_malos_repartidor')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error en reporte M: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()
