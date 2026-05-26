from datos.conexion import obtener_conexion


class RecuperacionDAO:
    def guardar(self, id_usuario, codigo, expira):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """REPLACE INTO RecuperacionPassword (id_usuario, codigo, expira, verificado)
                   VALUES (%s, %s, %s, 0)""",
                (id_usuario, codigo, expira)
            )
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
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_usuario, codigo, expira, verificado FROM RecuperacionPassword WHERE id_usuario = %s",
                (id_usuario,)
            )
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
            cursor.execute(
                "UPDATE RecuperacionPassword SET verificado = 1 WHERE id_usuario = %s",
                (id_usuario,)
            )
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
            cursor.execute(
                "DELETE FROM RecuperacionPassword WHERE id_usuario = %s",
                (id_usuario,)
            )
            conexion.commit()
            return True
        except Exception as e:
            print(f"[RecuperacionDAO] Error al eliminar: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()
