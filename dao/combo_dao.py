from datos.conexion import obtener_conexion


class ComboDAO:

    def guardar(self, combo):
        """combo es un dict con: id_restaurante, nombre, descripcion, numero, precio, imagen"""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """INSERT INTO Combo (id_restaurante, nombre, descripcion, numero, precio, imagen)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                valores = (
                    combo['id_restaurante'],
                    combo['nombre'],
                    combo.get('descripcion', ''),
                    combo['numero'],
                    combo['precio'],
                    combo.get('imagen', None)
                )
                cursor.execute(sql, valores)
                conexion.commit()
                return cursor.lastrowid
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
                sql = "SELECT * FROM Combo WHERE id_restaurante = %s ORDER BY numero"
                cursor.execute(sql, (id_restaurante,))
                return cursor.fetchall()
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
                sql = "SELECT * FROM OpcionCombo WHERE id_combo = %s"
                cursor.execute(sql, (id_combo,))
                opciones = cursor.fetchall()
                for opcion in opciones:
                    cursor2 = conexion.cursor(dictionary=True)
                    cursor2.execute("SELECT * FROM ValorOpcion WHERE id_opcion = %s", (opcion['id'],))
                    opcion['valores'] = cursor2.fetchall()
                    cursor2.close()
                return opciones
            except Exception as e:
                print(f"Error al listar opciones: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()