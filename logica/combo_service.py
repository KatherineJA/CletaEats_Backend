from dao.combo_dao import ComboDAO

combo_dao = ComboDAO()


class ComboService:

    def guardar_combo(self, id_restaurante, nombre, descripcion, numero, precio, imagen=None):
        try:
            id_nuevo = combo_dao.guardar({
                "id_restaurante": id_restaurante,
                "nombre": nombre,
                "descripcion": descripcion,
                "numero": numero,
                "precio": precio,
                "imagen": imagen
            })
            if id_nuevo:
                return {"exito": True, "mensaje": "Combo creado correctamente", "id": id_nuevo}
            return {"exito": False, "mensaje": "No se pudo crear el combo"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def actualizar_combo(self, id_combo, nombre, descripcion, numero, precio, imagen=None):
        try:
            resultado = combo_dao.actualizar({
                "id_combo": id_combo,
                "nombre": nombre,
                "descripcion": descripcion,
                "numero": numero,
                "precio": precio,
                "imagen": imagen
            })
            if resultado:
                return {"exito": True, "mensaje": "Combo actualizado correctamente"}
            return {"exito": False, "mensaje": "No se pudo actualizar el combo"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def eliminar_combo(self, id_combo):
        try:
            resultado = combo_dao.eliminar(id_combo)
            if resultado:
                return {"exito": True, "mensaje": "Combo eliminado correctamente"}
            return {"exito": False, "mensaje": "No se pudo eliminar el combo"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def listar_combos(self, id_restaurante):
        try:
            combos = combo_dao.listar_por_restaurante(id_restaurante)
            return {"exito": True, "combos": combos}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}", "combos": []}

    def detalle_combo(self, id_combo):
        try:
            opciones = combo_dao.listar_opciones_por_combo(id_combo)
            return {"exito": True, "opciones": opciones}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}", "opciones": []}

    def listar_opciones(self, id_combo):
        try:
            opciones = combo_dao.listar_opciones(id_combo)
            return {"exito": True, "opciones": opciones}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}", "opciones": []}

    def listar_valores_opcion(self, id_opcion):
        try:
            valores = combo_dao.listar_valores_opcion(id_opcion)
            return {"exito": True, "valores": valores}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}", "valores": []}

    def agregar_opcion_combo(self, id_combo, nombre, tipo):
        try:
            id_opcion = combo_dao.guardar_opcion(id_combo, nombre, tipo)
            if id_opcion:
                return {"exito": True, "mensaje": "Opción agregada correctamente", "id_opcion": id_opcion}
            return {"exito": False, "mensaje": "No se pudo agregar la opción"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def actualizar_opcion_combo(self, id_opcion, nombre, tipo):
        try:
            resultado = combo_dao.actualizar_opcion(id_opcion, nombre, tipo)
            if resultado:
                return {"exito": True, "mensaje": "Opción actualizada correctamente"}
            return {"exito": False, "mensaje": "No se pudo actualizar la opción"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def eliminar_opcion_combo(self, id_opcion):
        try:
            resultado = combo_dao.eliminar_opcion(id_opcion)
            if resultado:
                return {"exito": True, "mensaje": "Opción eliminada correctamente"}
            return {"exito": False, "mensaje": "No se pudo eliminar la opción"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def agregar_valor_opcion(self, id_opcion, descripcion, costo_adicional=0):
        try:
            id_valor = combo_dao.guardar_valor(id_opcion, descripcion, costo_adicional)
            if id_valor:
                return {"exito": True, "mensaje": "Valor agregado correctamente", "id_valor": id_valor}
            return {"exito": False, "mensaje": "No se pudo agregar el valor"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def actualizar_valor_opcion(self, id_valor, descripcion, costo_adicional=0):
        try:
            resultado = combo_dao.actualizar_valor(id_valor, descripcion, costo_adicional)
            if resultado:
                return {"exito": True, "mensaje": "Valor actualizado correctamente"}
            return {"exito": False, "mensaje": "No se pudo actualizar el valor"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}

    def eliminar_valor_opcion(self, id_valor):
        try:
            resultado = combo_dao.eliminar_valor(id_valor)
            if resultado:
                return {"exito": True, "mensaje": "Valor eliminado correctamente"}
            return {"exito": False, "mensaje": "No se pudo eliminar el valor"}
        except Exception as e:
            return {"exito": False, "mensaje": f"Error interno: {str(e)}"}
