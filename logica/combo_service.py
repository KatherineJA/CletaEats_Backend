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