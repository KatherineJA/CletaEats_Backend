from datos.conexion import obtener_conexion


class ReporteDAO:

    def clientes_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_clientes_registrados')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte A: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def restaurantes_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_restaurantes_registrados')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte B: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def repartidores_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_repartidores_registrados')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte C: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def pedidos_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_pedidos_registrados')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte D: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def clientes_activos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_clientes_activos')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte E: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def clientes_suspendidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_clientes_suspendidos')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte F: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def repartidores_sin_malos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_repartidores_sin_malos')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte G: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def restaurantes_listado(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_restaurantes_listado')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte H: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def restaurante_mas_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_restaurante_mas_pedidos')
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error reporte I: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def monto_por_restaurante(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_monto_por_restaurante')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte J: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def monto_total_global(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_monto_total_global')
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error reporte K: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def restaurante_menos_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_restaurante_menos_pedidos')
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error reporte L: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def malos_por_repartidor(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_malos_por_repartidor')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte M: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def pedidos_por_cliente(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_pedidos_por_cliente')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error reporte N: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def cliente_mas_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_cliente_mas_pedidos')
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error reporte O: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def hora_pico(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_reporte_hora_pico')
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error reporte P: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()