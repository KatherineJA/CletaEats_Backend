from datos.conexion import obtener_conexion


class PedidoDAO:

    def guardar(self, id_cliente, id_restaurante, lat_destino, lon_destino, distancia_km, costo_envio):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_pedido_guardar', (
                    id_cliente, id_restaurante,
                    lat_destino, lon_destino,
                    round(distancia_km, 4), costo_envio
                ))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
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
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_pedido_guardar_detalle', (id_pedido, id_combo, cantidad))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
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
                cursor.callproc('sp_pedido_guardar_preferencia', (id_detalle_pedido, id_valor_opcion))
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
                cursor.callproc('sp_pedido_actualizar_estado_completo',
                                (id_pedido, nuevo_estado, id_repartidor))
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
                cursor.callproc('sp_pedido_buscar_por_id', (id_pedido,))
                for result in cursor.stored_results():
                    return result.fetchone()
                return None
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
                cursor.callproc('sp_pedido_listar_por_cliente_activos', (id_cliente,))
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar pedidos por cliente: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_disponibles(self):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_pedido_listar_disponibles')
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar pedidos disponibles: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_por_repartidor(self, id_repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_pedido_listar_por_repartidor_activos', (id_repartidor,))
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar pedidos por repartidor: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_detalles(self, id_pedido):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_pedido_listar_detalles_con_preferencias', (id_pedido,))
                detalles = []
                for result in cursor.stored_results():
                    detalles = result.fetchall()

                for detalle in detalles:
                    cursor2 = conexion.cursor(dictionary=True)
                    cursor2.callproc('sp_pedido_preferencias_por_detalle', (detalle['id'],))
                    for r in cursor2.stored_results():
                        detalle['preferencias'] = r.fetchall()
                    cursor2.close()

                return detalles
            except Exception as e:
                print(f"Error al listar detalles: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def contar_pedidos_activos_repartidor(self, id_repartidor):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT fn_pedido_contar_activos_repartidor(%s)", (id_repartidor,))
                fila = cursor.fetchone()
                return fila[0] if fila else 0
            except Exception as e:
                print(f"Error al contar pedidos activos: {e}")
                return 0
            finally:
                cursor.close()
                conexion.close()
