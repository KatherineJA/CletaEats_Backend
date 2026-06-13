from datos.conexion import obtener_conexion
import psycopg2.extras

class ReporteDAO:

    def _fetchall(self, fn):
        conexion = obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(f"SELECT * FROM {fn}()")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error {fn}: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def _fetchone(self, fn):
        conexion = obtener_conexion()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(f"SELECT * FROM {fn}()")
            return cursor.fetchone()
        except Exception as e:
            print(f"Error {fn}: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def clientes_registrados(self):       return self._fetchall('sp_reporte_clientes_registrados')
    def restaurantes_registrados(self):   return self._fetchall('sp_reporte_restaurantes_registrados')
    def repartidores_registrados(self):   return self._fetchall('sp_reporte_repartidores_registrados')
    def pedidos_registrados(self):        return self._fetchall('sp_reporte_pedidos_registrados')
    def clientes_activos(self):           return self._fetchall('sp_reporte_clientes_activos')
    def clientes_suspendidos(self):       return self._fetchall('sp_reporte_clientes_suspendidos')
    def repartidores_sin_malos(self):     return self._fetchall('sp_reporte_repartidores_sin_malos')
    def restaurantes_listado(self):       return self._fetchall('sp_reporte_restaurantes_listado')
    def monto_por_restaurante(self):      return self._fetchall('sp_reporte_monto_por_restaurante')
    def malos_por_repartidor(self):       return self._fetchall('sp_reporte_malos_por_repartidor')
    def pedidos_por_cliente(self):        return self._fetchall('sp_reporte_pedidos_por_cliente')
    def restaurante_mas_pedidos(self):    return self._fetchone('sp_reporte_restaurante_mas_pedidos')
    def monto_total_global(self):         return self._fetchone('sp_reporte_monto_total_global')
    def restaurante_menos_pedidos(self):  return self._fetchone('sp_reporte_restaurante_menos_pedidos')
    def cliente_mas_pedidos(self):        return self._fetchone('sp_reporte_cliente_mas_pedidos')
    def hora_pico(self):                  return self._fetchone('sp_reporte_hora_pico')