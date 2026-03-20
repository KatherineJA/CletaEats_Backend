from datos.conexion import obtener_conexion
from modelo.cliente import Cliente

class ClienteDAO:

    def guardar(self, cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO cliente 
                         (usuario_id, cedula, nombre, direccion, tarjeta, telefono, estado) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    cliente.usuario_id,
                    cliente.get_cedula(),
                    cliente.get_nombre(),
                    cliente.direccion,
                    cliente.tarjeta,
                    cliente.telefono,
                    cliente.get_estado()
                )
                cursor.execute(sql, valores)
                conexion.commit()
                cliente.set_id(cursor.lastrowid)
                return cliente
            except Exception as e:
                print(f"Error al guardar cliente: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula(self, cedula):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "SELECT id, usuario_id, cedula, nombre, direccion, tarjeta, telefono, estado FROM cliente WHERE cedula = %s"
                cursor.execute(sql, (cedula,))
                fila = cursor.fetchone()
                if fila:
                    c = Cliente()
                    c.set_id(fila[0])
                    c.usuario_id = fila[1]
                    c.set_cedula(fila[2])
                    c.set_nombre(fila[3])
                    c.direccion = fila[4]
                    c.tarjeta = fila[5]
                    c.telefono = fila[6]
                    c.set_estado(fila[7])
                    return c
                return None
            except Exception as e:
                print(f"Error al buscar cliente: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()