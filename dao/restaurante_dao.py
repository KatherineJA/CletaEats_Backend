from datos.conexion import obtener_conexion
from modelo.restaurante import Restaurante


class RestauranteDAO:

    def guardar(self, restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_restaurante_guardar', (
                    restaurante.nombre,
                    restaurante.cedula_juridica,
                    restaurante.direccion,
                    restaurante.tipo_comida,
                    restaurante.latitud,
                    restaurante.longitud,
                    restaurante.imagen,
                ))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    if fila:
                        restaurante.set_id(fila['id'])
                return restaurante
            except Exception as e:
                print(f"Error al guardar restaurante: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def listar_todos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_restaurante_listar_todos')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar restaurantes: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_cedula_juridica(self, cedula_juridica):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.callproc('sp_restaurante_buscar_por_cedula_juridica', (cedula_juridica,))
                for result in cursor.stored_results():
                    return result.fetchone() is not None
                return False
            except Exception as e:
                print(f"Error al buscar restaurante: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_restaurante_buscar_por_id', (id_restaurante,))
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
            except Exception as e:
                print(f"Error al buscar restaurante por id: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_encargado(self, id_restaurante, id_encargado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                # Ejecuta los UPDATE de la tabla intermedia de manera limpia
                cursor.callproc('sp_restaurante_actualizar_encargado', (
                    id_restaurante,
                    id_encargado
                ))
                conexion.commit()

                # Si llegó hasta aquí sin excepciones, la base de datos guardó los cambios con éxito
                return True
            except Exception as e:
                print(f"Error al actualizar encargado de restaurante: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()
        return False