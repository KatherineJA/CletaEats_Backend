from datos.conexion import obtener_conexion
from modelo.cliente import Cliente


class ClienteDAO:

    def guardar(self, cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO Cliente (id_usuario, numero_tarjeta, estado) VALUES (%s, %s, %s)"
                valores = (cliente.id_usuario, cliente.numero_tarjeta, cliente.estado)
                cursor.execute(sql, valores)
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
                cursor.execute("SELECT id_usuario, numero_tarjeta, estado FROM Cliente WHERE id_usuario = %s", (id_usuario,))
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
                cursor.execute("UPDATE Cliente SET estado = %s WHERE id_usuario = %s", (estado, id_usuario))
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
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT u.id, u.cedula, u.nombre
                         FROM Usuario u JOIN Cliente c ON u.id = c.id_usuario
                         WHERE c.estado = 'ACTIVO'"""
                cursor.execute(sql)
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
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT u.id, u.cedula, u.nombre
                         FROM Usuario u JOIN Cliente c ON u.id = c.id_usuario
                         WHERE c.estado = 'SUSPENDIDO'"""
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar clientes suspendidos: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()