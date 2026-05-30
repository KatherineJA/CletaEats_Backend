from datos.conexion import obtener_conexion


class EncargadoDAO:

    def guardar(self, id_usuario, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.callproc('sp_encargado_guardar', (id_usuario, id_restaurante))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al guardar encargado: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_encargado_buscar_por_id', (id_usuario,))
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error al buscar encargado: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def buscar_restaurante_de_encargado(self, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.callproc('sp_encargado_buscar_restaurante', (id_usuario,))
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila[0] if fila else None
                return None
            except Exception as e:
                print(f"Error al buscar restaurante del encargado: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()
