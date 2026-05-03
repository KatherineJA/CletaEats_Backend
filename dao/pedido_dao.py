from datos.conexion import obtener_conexion


class PedidoDAO:

    def guardar(self, id_cliente, id_restaurante, lat_destino, lon_destino, distancia_km, costo_envio):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Pedido (id_cliente, id_restaurante, estado,
                                             latitud_destino, longitud_destino, distancia_km, costo_envio)
                         VALUES (%s, %s, 'EN_PREPARACION', %s, %s, %s, %s)"""
                cursor.execute(sql, (id_cliente, id_restaurante, lat_destino, lon_destino,
                                     round(distancia_km, 4), costo_envio))
                conexion.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error al guardar pedido: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def guardar_detalle(self, id_pedido, id_combo, cantidad):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""INSERT INTO DetallePedido (id_pedido, id_combo, cantidad)
                                  VALUES (%s, %s, %s)""", (id_pedido, id_combo, cantidad))
                conexion.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error al guardar detalle: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def guardar_preferencia(self, id_detalle_pedido, id_valor_opcion):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""INSERT INTO PreferenciaDetalle (id_detalle_pedido, id_valor_opcion)
                                  VALUES (%s, %s)""", (id_detalle_pedido, id_valor_opcion))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al guardar preferencia: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def actualizar_estado(self, id_pedido, nuevo_estado, id_repartidor=None):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                if nuevo_estado == "EN_CAMINO" and id_repartidor:
                    cursor.execute("""UPDATE Pedido SET estado = %s, id_repartidor = %s
                                      WHERE id = %s""", (nuevo_estado, id_repartidor, id_pedido))
                elif nuevo_estado == "ENTREGADO":
                    cursor.execute("""UPDATE Pedido SET estado = %s, hora_entrega = NOW()
                                      WHERE id = %s""", (nuevo_estado, id_pedido))
                else:
                    cursor.execute("UPDATE Pedido SET estado = %s WHERE id = %s",
                                   (nuevo_estado, id_pedido))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar estado pedido: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def buscar_por_id(self, id_pedido):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Pedido WHERE id = %s", (id_pedido,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error al buscar pedido: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def listar_por_cliente(self, id_cliente):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT p.*, r.nombre AS nombre_restaurante
                         FROM Pedido p
                         JOIN Restaurante r ON p.id_restaurante = r.id
                         WHERE p.id_cliente = %s
                         ORDER BY p.hora_creacion DESC"""
                cursor.execute(sql, (id_cliente,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar pedidos por cliente: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_por_repartidor(self, id_repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT p.*, r.nombre AS nombre_restaurante
                         FROM Pedido p
                         JOIN Restaurante r ON p.id_restaurante = r.id
                         WHERE p.id_repartidor = %s
                         ORDER BY p.hora_creacion DESC"""
                cursor.execute(sql, (id_repartidor,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar pedidos por repartidor: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_disponibles(self):
        """Pedidos EN_PREPARACION sin repartidor asignado."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT p.*, r.nombre AS nombre_restaurante,
                                r.latitud AS lat_restaurante, r.longitud AS lon_restaurante
                         FROM Pedido p
                         JOIN Restaurante r ON p.id_restaurante = r.id
                         WHERE p.estado = 'EN_PREPARACION' AND p.id_repartidor IS NULL
                         ORDER BY p.hora_creacion ASC"""
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar pedidos disponibles: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_detalles(self, id_pedido):
        """Combos + preferencias de un pedido, para mostrar en la factura."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                sql = """SELECT dp.id, dp.cantidad, c.nombre AS combo, c.precio,
                                c.numero AS numero_combo
                         FROM DetallePedido dp
                         JOIN Combo c ON dp.id_combo = c.id
                         WHERE dp.id_pedido = %s"""
                cursor.execute(sql, (id_pedido,))
                detalles = cursor.fetchall()
                for detalle in detalles:
                    cursor2 = conexion.cursor(dictionary=True)
                    cursor2.execute("""SELECT vo.descripcion, vo.costo_adicional, oc.nombre AS opcion
                                       FROM PreferenciaDetalle pd
                                       JOIN ValorOpcion vo ON pd.id_valor_opcion = vo.id
                                       JOIN OpcionCombo oc ON vo.id_opcion = oc.id
                                       WHERE pd.id_detalle_pedido = %s""", (detalle['id'],))
                    detalle['preferencias'] = cursor2.fetchall()
                    cursor2.close()
                return detalles
            except Exception as e:
                print(f"Error al listar detalles: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def contar_pedidos_activos_repartidor(self, id_repartidor):
        """Cuenta pedidos EN_CAMINO del repartidor. Debe ser 0 para aceptar uno nuevo."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""SELECT COUNT(*) FROM Pedido
                                  WHERE id_repartidor = %s AND estado = 'EN_CAMINO'""",
                               (id_repartidor,))
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error al contar pedidos activos: {e}")
                return 0
            finally:
                cursor.close()
                conexion.close()