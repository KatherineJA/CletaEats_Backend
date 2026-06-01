from datos.conexion import obtener_conexion


class ComboDAO:

    def guardar(self, combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)

                # Forzar la conversión limpia de datos para evitar desajustes en el SP
                id_restaurante = int(combo['id_restaurante'])
                nombre = str(combo['nombre'])
                descripcion = str(combo.get('descripcion', ''))
                numero = int(combo['numero']) if combo.get('numero') is not None else 0
                precio = float(combo['precio'])
                imagen = combo.get('imagen', None)
                if imagen:
                    imagen = str(imagen)

                cursor.callproc('sp_combo_guardar', (
                    id_restaurante,
                    nombre,
                    descripcion,
                    numero,
                    precio,
                    imagen
                ))
                conexion.commit()

                for result in cursor.stored_results():
                    fila = result.fetchone()
                    return fila['id'] if fila else None
            except Exception as e:
                print(f"Error crítico al guardar combo en BD: {e}")
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

    # ── MÉTODOS CORREGIDOS (Se agregó la sangría para meterlos en la clase) ──
    def actualizar(self, combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_actualizar', (
                    combo['id_combo'],
                    combo['nombre'],
                    combo.get('descripcion', ''),
                    combo['numero'],
                    combo['precio'],
                    combo.get('imagen', None)
                ))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar combo: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()

    def eliminar(self, id_combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.callproc('sp_combo_eliminar', (id_combo,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar combo: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()