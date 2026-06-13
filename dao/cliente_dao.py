from datos.conexion import obtener_conexion
from modelo.cliente import Cliente
import psycopg2.extras

class ClienteDAO:

    def guardar(self, cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_cliente_guardar(%s,%s,%s)",
                               (cliente.id_usuario, cliente.numero_tarjeta, cliente.estado))
                conexion.commit()
                return cliente
            except Exception as e:
                print(f"Error al guardar cliente: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM sp_cliente_buscar_por_id(%s)", (id_usuario,))
                fila = cursor.fetchone()
                if fila:
                    c = Cliente()
                    c.id_usuario, c.numero_tarjeta, c.estado = fila
                    return c
                return None
            except Exception as e:
                print(f"Error al buscar cliente: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_estado(self, id_usuario, estado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_cliente_actualizar_estado(%s,%s)", (id_usuario, estado))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar estado cliente: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def listar_activos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_cliente_listar_activos()")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar clientes activos: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_suspendidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_cliente_listar_suspendidos()")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar clientes suspendidos: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()