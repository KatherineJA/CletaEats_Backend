from datos.conexion import obtener_conexion
from modelo.usuario import Usuario


class UsuarioDAO:

    def guardar(self, usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Usuario (cedula, nombre, correo, contrasena, telefono, rol, latitud, longitud)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    usuario.cedula, usuario.nombre, usuario.correo, usuario.contrasena,
                    usuario.telefono, usuario.rol, usuario.latitud, usuario.longitud
                )
                cursor.execute(sql, valores)
                conexion.commit()
                usuario.set_id(cursor.lastrowid)
                return usuario
            except Exception as e:
                print(f"Error al guardar usuario: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_correo(self, correo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""SELECT id, cedula, nombre, correo, contrasena, telefono, rol, latitud, longitud
                                  FROM Usuario WHERE correo = %s""", (correo,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.id, u.cedula, u.nombre, u.correo, u.contrasena, u.telefono, u.rol, u.latitud, u.longitud = fila
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula(self, cedula):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id FROM Usuario WHERE cedula = %s", (cedula,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error al buscar por cédula: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""SELECT id, cedula, nombre, correo, contrasena, telefono, rol, latitud, longitud
                                  FROM Usuario WHERE id = %s""", (id_usuario,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.id, u.cedula, u.nombre, u.correo, u.contrasena, u.telefono, u.rol, u.latitud, u.longitud = fila
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario por id: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_perfil(self, id_usuario, telefono, latitud=None, longitud=None):
        """Actualiza teléfono y ubicación del usuario."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""UPDATE Usuario SET telefono = %s, latitud = %s, longitud = %s
                                  WHERE id = %s""", (telefono, latitud, longitud, id_usuario))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar perfil: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_tarjeta_cliente(self, id_usuario, numero_tarjeta):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE Cliente SET numero_tarjeta = %s WHERE id_usuario = %s",
                               (numero_tarjeta, id_usuario))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar tarjeta cliente: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_tarjeta_repartidor(self, id_usuario, numero_tarjeta):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE Repartidor SET numero_tarjeta = %s WHERE id_usuario = %s",
                               (numero_tarjeta, id_usuario))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar tarjeta repartidor: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()