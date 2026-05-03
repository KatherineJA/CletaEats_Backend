from datos.conexion import obtener_conexion


class ReporteDAO:
    """
    Contiene todas las queries de los reportes definidos en el documento
    (sección 8, ítems a–p). Todos son de solo lectura (SELECT).
    """

    # ------------------------------------------------------------------
    # a) Registro de clientes
    # ------------------------------------------------------------------
    def clientes_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre, u.correo, u.telefono, c.estado
                    FROM Usuario u
                    JOIN Cliente c ON u.id = c.id_usuario
                    ORDER BY u.id
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte A: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # b) Registro de restaurantes
    # ------------------------------------------------------------------
    def restaurantes_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id, nombre, cedula_juridica, direccion, tipo_comida
                    FROM Restaurante
                    ORDER BY id
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte B: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # c) Registro de repartidores
    # ------------------------------------------------------------------
    def repartidores_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre, u.correo, u.telefono, r.estado, r.kilometros_diarios
                    FROM Usuario u
                    JOIN Repartidor r ON u.id = r.id_usuario
                    ORDER BY u.id
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte C: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # d) Registro de pedidos
    # ------------------------------------------------------------------
    def pedidos_registrados(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT p.id, p.estado, p.hora_creacion, p.hora_entrega,
                           p.distancia_km, p.costo_envio,
                           uc.nombre AS cliente, ur.nombre AS repartidor,
                           r.nombre AS restaurante
                    FROM Pedido p
                    JOIN Usuario uc ON p.id_cliente = uc.id
                    JOIN Restaurante r ON p.id_restaurante = r.id
                    LEFT JOIN Usuario ur ON p.id_repartidor = ur.id
                    ORDER BY p.hora_creacion DESC
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte D: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # e) Clientes activos: id, cédula, nombre
    # ------------------------------------------------------------------
    def clientes_activos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre
                    FROM Usuario u
                    JOIN Cliente c ON u.id = c.id_usuario
                    WHERE c.estado = 'ACTIVO'
                    ORDER BY u.nombre
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte E: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # f) Clientes suspendidos: id, cédula, nombre
    # ------------------------------------------------------------------
    def clientes_suspendidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre
                    FROM Usuario u
                    JOIN Cliente c ON u.id = c.id_usuario
                    WHERE c.estado = 'SUSPENDIDO'
                    ORDER BY u.nombre
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte F: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # g) Repartidores con cero calificaciones MALO
    # ------------------------------------------------------------------
    def repartidores_sin_malos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre
                    FROM Usuario u
                    JOIN Repartidor r ON u.id = r.id_usuario
                    WHERE (
                        SELECT COUNT(*) FROM Calificacion
                        WHERE id_evaluado = u.id AND tipo = 'MALO'
                    ) = 0
                    ORDER BY u.nombre
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte G: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # h) Listado de restaurantes: nombre, cédula jurídica, dirección, tipo
    # ------------------------------------------------------------------
    def restaurantes_listado(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT nombre, cedula_juridica, direccion, tipo_comida
                    FROM Restaurante
                    ORDER BY nombre
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte H: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # i) Restaurante con mayor número de pedidos
    # ------------------------------------------------------------------
    def restaurante_mas_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT r.id, r.nombre, r.tipo_comida, COUNT(p.id) AS total_pedidos
                    FROM Restaurante r
                    JOIN Pedido p ON r.id = p.id_restaurante
                    GROUP BY r.id, r.nombre, r.tipo_comida
                    ORDER BY total_pedidos DESC
                    LIMIT 1
                """)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error reporte I: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # j) Monto total vendido por cada restaurante
    # ------------------------------------------------------------------
    def monto_por_restaurante(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT r.id, r.nombre,
                           COALESCE(SUM(p.costo_envio), 0) AS total_envios,
                           COALESCE(SUM(
                               (SELECT SUM(dp.cantidad * c.precio)
                                FROM DetallePedido dp
                                JOIN Combo c ON dp.id_combo = c.id
                                WHERE dp.id_pedido = p.id)
                           ), 0) AS total_subtotales
                    FROM Restaurante r
                    LEFT JOIN Pedido p ON r.id = p.id_restaurante
                        AND p.estado NOT IN ('CANCELADO')
                    GROUP BY r.id, r.nombre
                    ORDER BY total_subtotales DESC
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte J: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # k) Monto total vendido por todos los restaurantes
    # ------------------------------------------------------------------
    def monto_total_global(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT
                        COALESCE(SUM(
                            (SELECT SUM(dp.cantidad * c.precio)
                             FROM DetallePedido dp
                             JOIN Combo c ON dp.id_combo = c.id
                             WHERE dp.id_pedido = p.id)
                        ), 0) AS total_subtotales,
                        COALESCE(SUM(p.costo_envio), 0) AS total_envios
                    FROM Pedido p
                    WHERE p.estado NOT IN ('CANCELADO')
                """)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error reporte K: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # l) Restaurante con menor número de pedidos
    # ------------------------------------------------------------------
    def restaurante_menos_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT r.id, r.nombre, r.tipo_comida, COUNT(p.id) AS total_pedidos
                    FROM Restaurante r
                    LEFT JOIN Pedido p ON r.id = p.id_restaurante
                    GROUP BY r.id, r.nombre, r.tipo_comida
                    ORDER BY total_pedidos ASC
                    LIMIT 1
                """)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error reporte L: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # m) Calificaciones MALO por cada repartidor
    # ------------------------------------------------------------------
    def malos_por_repartidor(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre,
                           COUNT(c.id) AS total_malos,
                           GROUP_CONCAT(c.opinion SEPARATOR ' | ') AS opiniones
                    FROM Usuario u
                    JOIN Repartidor r ON u.id = r.id_usuario
                    LEFT JOIN Calificacion c ON c.id_evaluado = u.id AND c.tipo = 'MALO'
                    GROUP BY u.id, u.cedula, u.nombre
                    ORDER BY total_malos DESC
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte M: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # n) Listado de pedidos por cada cliente
    # ------------------------------------------------------------------
    def pedidos_por_cliente(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre,
                           COUNT(p.id) AS total_pedidos
                    FROM Usuario u
                    JOIN Cliente c ON u.id = c.id_usuario
                    LEFT JOIN Pedido p ON p.id_cliente = u.id
                    GROUP BY u.id, u.cedula, u.nombre
                    ORDER BY total_pedidos DESC
                """)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error reporte N: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # o) Cliente con mayor número de pedidos
    # ------------------------------------------------------------------
    def cliente_mas_pedidos(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.id, u.cedula, u.nombre, COUNT(p.id) AS total_pedidos
                    FROM Usuario u
                    JOIN Cliente c ON u.id = c.id_usuario
                    JOIN Pedido p ON p.id_cliente = u.id
                    GROUP BY u.id, u.cedula, u.nombre
                    ORDER BY total_pedidos DESC
                    LIMIT 1
                """)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error reporte O: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------------------------
    # p) Hora pico: hora en que se realizaron más pedidos
    # ------------------------------------------------------------------
    def hora_pico(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""
                    SELECT HOUR(hora_creacion) AS hora, COUNT(*) AS total_pedidos
                    FROM Pedido
                    GROUP BY hora
                    ORDER BY total_pedidos DESC
                    LIMIT 1
                """)
                return cursor.fetchone()
            except Exception as e:
                print(f"Error reporte P: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()