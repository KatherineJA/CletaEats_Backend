from datos.conexion import obtener_conexion
import psycopg2.extras

class ComboDAO:

    def guardar(self, combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT sp_combo_guardar(%s::integer, %s::varchar, %s::text, %s::smallint, %s::decimal, %s::varchar)",
                    (
                        int(combo['id_restaurante']),
                        str(combo['nombre']),
                        str(combo.get('descripcion', '') or ''),
                        int(combo.get('numero', 0)),
                        float(combo['precio']),
                        combo.get('imagen') or None
                    )
                )
                fila = cursor.fetchone()
                conexion.commit()
                return fila[0] if fila else None
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
                cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT * FROM sp_combo_listar_por_restaurante(%s)", (id_restaurante,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar combos: {e}")
                return []
            finally:
                cursor.close()
                conexion.close()

    def listar_opciones_por_combo(self, id_combo):
        opciones = self.listar_opciones(id_combo)
        for opcion in opciones:
            opcion['valores'] = self.listar_valores_opcion(opcion['id'])
        return opciones

    def listar_opciones(self, id_combo):
        conexion = obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM sp_combo_listar_opciones(%s)", (id_combo,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listar_opciones: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def listar_valores_opcion(self, id_opcion):
        conexion = obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM sp_combo_listar_valores_opcion(%s)", (id_opcion,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listar_valores_opcion: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def guardar_opcion(self, id_combo, nombre, tipo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_combo_guardar_opcion(%s,%s,%s)", (id_combo, nombre, tipo))
                fila = cursor.fetchone()
                conexion.commit()
                return fila[0] if fila else None
            except Exception as e:
                print(f"Error al guardar opción: {e}")
                return None
            finally:
                cursor.close()
                conexion.close()

    def actualizar_opcion(self, id_opcion, nombre, tipo):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_combo_actualizar_opcion(%s,%s,%s)", (id_opcion, nombre, tipo))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error actualizar_opcion: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar_opcion(self, id_opcion):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_combo_eliminar_opcion(%s)", (id_opcion,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error eliminar_opcion: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def guardar_valor(self, id_opcion, descripcion, costo_adicional):
        conexion = obtener_conexion()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_combo_guardar_valor_opcion(%s,%s,%s)", (id_opcion, descripcion, float(costo_adicional)))
            fila = cursor.fetchone()
            conexion.commit()
            return fila[0] if fila else None
        except Exception as e:
            print(f"Error guardar_valor: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def guardar_valor_opcion(self, id_opcion, descripcion, costo_adicional=0):
        return self.guardar_valor(id_opcion, descripcion, costo_adicional)

    def actualizar_valor(self, id_valor, descripcion, costo_adicional):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_combo_actualizar_valor_opcion(%s,%s,%s)", (id_valor, descripcion, float(costo_adicional)))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error actualizar_valor: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar_valor(self, id_valor):
        conexion = obtener_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT sp_combo_eliminar_valor_opcion(%s)", (id_valor,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error eliminar_valor: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def actualizar(self, combo):
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_combo_actualizar(%s,%s,%s,%s,%s,%s)", (
                    combo['id_combo'], combo['nombre'], combo.get('descripcion', ''),
                    combo['numero'], combo['precio'], combo.get('imagen')
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
                cursor = conexion.cursor()
                cursor.execute("SELECT sp_combo_eliminar(%s)", (id_combo,))
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar combo: {e}")
                return False
            finally:
                cursor.close()
                conexion.close()