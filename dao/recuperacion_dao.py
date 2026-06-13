from datos.conexion import obtener_conexion
import psycopg2.extras

class RecuperacionDAO:

    def guardar(self, id_usuario, codigo, expira):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_recuperacion_guardar(%s,%s,%s)", (id_usuario, codigo, expira))
            conexion.commit()
            return True
        except Exception as e:
            print(f"[RecuperacionDAO] Error al guardar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def buscar_por_usuario(self, id_usuario):
        conexion = obtener_conexion()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM sp_recuperacion_buscar_por_usuario(%s)", (id_usuario,))
            return cursor.fetchone()
        except Exception as e:
            print(f"[RecuperacionDAO] Error al buscar: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def marcar_verificado(self, id_usuario):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_recuperacion_marcar_verificado(%s)", (id_usuario,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"[RecuperacionDAO] Error al marcar verificado: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar(self, id_usuario):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_recuperacion_eliminar(%s)", (id_usuario,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"[RecuperacionDAO] Error al eliminar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()