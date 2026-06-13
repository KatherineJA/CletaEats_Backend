from datos.conexion import obtener_conexion
from modelo.usuario import Usuario
import psycopg2.extras

class UsuarioDAO:

    def guardar(self, usuario):
        conexion = obtener_conexion()

        print("Conexion:", conexion)

        if conexion:
            try:
                cursor = conexion.cursor()

                print("Intentando guardar usuario:", usuario.correo)

                cursor.execute(
                    "SELECT sp_usuario_guardar(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        usuario.cedula,
                        usuario.nombre,
                        usuario.correo,
                        usuario.contrasena,
                        usuario.telefono,
                        usuario.rol,
                        usuario.latitud,
                        usuario.longitud
                    )
                )

                print("SP ejecutado correctamente")

                fila = cursor.fetchone()
                print("Fila retornada:", fila)

                if fila:
                    usuario.set_id(fila[0])

                conexion.commit()
                return usuario

            except Exception as e:
                print("ERROR COMPLETO:")
                print(type(e))
                print(e)
                return None

    def buscar_por_correo(self, correo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM sp_usuario_buscar_por_correo(%s)", (correo,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.id, u.cedula, u.nombre, u.correo, u.contrasena, \
                    u.telefono, u.rol, u.latitud, u.longitud, u.foto_perfil = fila
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario por correo: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_telefono(self, telefono):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM sp_usuario_buscar_por_telefono(%s)", (telefono,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.id, u.cedula, u.nombre, u.correo, u.contrasena, \
                    u.telefono, u.rol, u.latitud, u.longitud, u.foto_perfil = fila
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario por telefono: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula(self, cedula):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM sp_usuario_buscar_por_cedula(%s)", (cedula,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error al buscar por cedula: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM sp_usuario_buscar_por_id(%s)", (id_usuario,))
                fila = cursor.fetchone()
                if fila:
                    u = Usuario()
                    u.id, u.cedula, u.nombre, u.correo, u.contrasena, \
                    u.telefono, u.rol, u.latitud, u.longitud, u.foto_perfil = fila
                    return u
                return None
            except Exception as e:
                print(f"Error al buscar usuario por id: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_perfil(self, id_usuario, telefono, latitud=None, longitud=None):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_actualizar_perfil(%s,%s,%s,%s)", (id_usuario, telefono, latitud, longitud))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar perfil: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_foto(self, id_usuario, url_foto):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_actualizar_foto(%s,%s)", (id_usuario, url_foto))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar foto: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_nombre(self, id_usuario, nombre):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_actualizar_nombre(%s,%s)", (id_usuario, nombre))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar nombre: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_contrasena(self, id_usuario, contrasena_hash):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_actualizar_contrasena(%s,%s)", (id_usuario, contrasena_hash))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar contrasena: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_tarjeta_cliente(self, id_usuario, numero_tarjeta):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_actualizar_tarjeta_cliente(%s,%s)", (id_usuario, numero_tarjeta))
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
                cursor.execute("SELECT sp_usuario_actualizar_tarjeta_repartidor(%s,%s)", (id_usuario, numero_tarjeta))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar tarjeta repartidor: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def listar_por_rol_y_estado(self, rol, estado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_usuario_listar_por_rol_y_estado(%s,%s)", (rol, estado))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar por rol y estado: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def cambiar_estado_cliente(self, id_usuario, nuevo_estado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_usuario_cambiar_estado_cliente(%s,%s)", (id_usuario, nuevo_estado))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al cambiar estado cliente: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()