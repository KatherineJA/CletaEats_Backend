from datos.conexion import obtener_conexion
from modelo.restaurante import Restaurante
import psycopg2.extras


class RestauranteDAO:

    def guardar(self, restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT sp_restaurante_guardar(
                        %s,%s,%s,%s,%s,%s,%s
                    )
                    """,
                    (
                        restaurante.nombre,
                        restaurante.cedula_juridica,
                        restaurante.direccion,
                        restaurante.tipo_comida,
                        restaurante.latitud,
                        restaurante.longitud,
                        restaurante.imagen
                    )
                )

                fila = cursor.fetchone()

                if fila:
                    restaurante.set_id(fila[0])

                conexion.commit()
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
                cursor = conexion.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                cursor.execute(
                    "SELECT * FROM sp_restaurante_listar_todos()"
                )

                return cursor.fetchall()

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

                cursor.execute(
                    """
                    SELECT *
                    FROM sp_restaurante_buscar_por_cedula_juridica(%s)
                    """,
                    (cedula_juridica,)
                )

                return cursor.fetchone() is not None

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
                cursor = conexion.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )

                cursor.execute(
                    """
                    SELECT *
                    FROM sp_restaurante_buscar_por_id(%s)
                    """,
                    (id_restaurante,)
                )

                return cursor.fetchone()

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
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT sp_restaurante_actualizar_encargado(
                        %s,%s
                    )
                    """,
                    (
                        id_restaurante,
                        id_encargado
                    )
                )

                conexion.commit()
                return True

            except Exception as e:
                print(f"Error al actualizar encargado: {e}")
                return False

            finally:
                cursor.close()
                conexion.close()

        return False

    def actualizar_datos(self, id_restaurante, nombre, direccion, tipo_comida, imagen):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT sp_restaurante_actualizar(%s, %s, %s, %s, %s)",
                    (id_restaurante, nombre, direccion, tipo_comida, imagen)
                )
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar restaurante: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()
        return False