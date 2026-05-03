from datos.conexion import obtener_conexion


class CalificacionDAO:

    def guardar(self, id_pedido, id_evaluador, id_evaluado, rol_evaluador, tipo, opinion=""):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Calificacion (id_pedido, id_evaluador, id_evaluado,
                                                   rol_evaluador, tipo, opinion)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (id_pedido, id_evaluador, id_evaluado,
                                     rol_evaluador, tipo, opinion))
                conexion.commit()
                return True
            except Exception as e:
                if "Duplicate entry" in str(e):
                    raise ValueError("Ya existe una calificación de este evaluador para este pedido")
                print(f"Error al guardar calificación: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def contar_malos_por_evaluado(self, id_evaluado):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""SELECT COUNT(*) FROM Calificacion
                                  WHERE id_evaluado = %s AND tipo = 'MALO'""", (id_evaluado,))
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error al contar calificaciones MALO: {e}")
                return 0
            finally:
                cursor.close()
                conexion.close()

    def listar_por_pedido(self, id_pedido):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT c.*, u.nombre AS nombre_evaluador
                         FROM Calificacion c
                         JOIN Usuario u ON c.id_evaluador = u.id
                         WHERE c.id_pedido = %s"""
                cursor.execute(sql, (id_pedido,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar calificaciones: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_malos_por_repartidor(self):
        """Reporte M: calificaciones MALO agrupadas por repartidor."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT u.id, u.cedula, u.nombre,
                                COUNT(c.id) AS total_malos
                         FROM Usuario u
                         JOIN Repartidor r ON u.id = r.id_usuario
                         LEFT JOIN Calificacion c ON c.id_evaluado = u.id AND c.tipo = 'MALO'
                         GROUP BY u.id, u.cedula, u.nombre
                         ORDER BY total_malos DESC"""
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error en reporte M: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()