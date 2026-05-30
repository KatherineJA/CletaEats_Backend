from datos.conexion import obtener_conexion


class ComboDAO:

    def guardar(self, combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_guardar', (
                    combo['id_restaurante'],
                    combo['nombre'],
                    combo.get('descripcion', ''),
                    combo['numero'],
                    combo['precio'],
                    combo.get('imagen', None)
                ))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
            except Exception as e:
                print(f"Error al guardar combo: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def listar_por_restaurante(self, id_restaurante):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_listar_por_restaurante', (id_restaurante,))
                for result in cursor.stored_results():
                    return result.fetchall()
                return []
            except Exception as e:
                print(f"Error al listar combos: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_opciones_por_combo(self, id_combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_listar_opciones', (id_combo,))
                opciones = []
                for result in cursor.stored_results():
                    opciones = result.fetchall()

                for opcion in opciones:
                    cursor2 = conexion.cursor(dictionary=True)
                    cursor2.callproc('sp_combo_listar_valores_opcion', (opcion['id'],))
                    for r in cursor2.stored_results():
                        opcion['valores'] = r.fetchall()
                    cursor2.close()

                return opciones
            except Exception as e:
                print(f"Error al listar opciones: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def guardar_opcion(self, id_combo, nombre, tipo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_guardar_opcion', (id_combo, nombre, tipo))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
            except Exception as e:
                print(f"Error al guardar opción: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def guardar_valor_opcion(self, id_opcion, descripcion, costo_adicional=0):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_guardar_valor_opcion', (id_opcion, descripcion, costo_adicional))
                conexion.commit()
                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
            except Exception as e:
                print(f"Error al guardar valor opción: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()
