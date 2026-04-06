from datos.conexion import obtener_conexion
from modelo.usuario import Usuario


class UsuarioDAO:

    def guardar(self, usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO usuario (correo, password_hash, rol) VALUES (%s, %s, %s)"
                valores = (usuario.get_correo(), usuario.password_hash, usuario.get_rol())
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

    def crear_usuario(self, correo, password, rol):
        u = Usuario()
        u.set_correo(correo)
        u.password_hash = password  # En producción deberías usar hash
        u.set_rol(rol)

        resultado = self.guardar(u)
        if resultado:
            return resultado.get_id()  # Retornamos el ID para la tabla repartidor
        return None

    def buscar_por_correo(self, correo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "SELECT id, correo, password_hash, rol FROM usuario WHERE correo = %s"
                cursor.execute(sql, (correo,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.set_id(fila[0])
                    u.set_correo(fila[1])
                    u.password_hash = fila[2]
                    u.set_rol(fila[3])
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()