from dao.combo_dao import ComboDAO

combo_dao = ComboDAO()


class ComboService:

    @staticmethod
    def _resolver_imagen_url(imagen):
        if not imagen:
            return None
        if isinstance(imagen, str) and (imagen.startswith("http://") or imagen.startswith("https://") or imagen.startswith("/")):
            return imagen
        return f"/{imagen}"

    def _adjuntar_imagen_url(self, combo):
        imagen = combo.get("imagen") if isinstance(combo, dict) else None
        combo["imagen_url"] = self._resolver_imagen_url(imagen)
        return combo

    @staticmethod
    def _normalizar_valor_predefinido(valor):
        if isinstance(valor, dict):
            descripcion = valor.get("descripcion", "")
            costo_adicional = valor.get("costo_adicional", 0)
        else:
            descripcion = str(valor)
            costo_adicional = 0
        return str(descripcion).strip(), costo_adicional

    def _guardar_opciones_predefinidas(self, id_combo, opciones_predefinidas):
        resumen = {"opciones_creadas": 0, "valores_creados": 0, "errores": []}
        if not opciones_predefinidas:
            return resumen

        for indice, opcion in enumerate(opciones_predefinidas, start=1):
            if not isinstance(opcion, dict):
                resumen["errores"].append(f"Opción #{indice} inválida")
                continue

            nombre = str(opcion.get("nombre", "")).strip()
            tipo = str(opcion.get("tipo", "")).strip()
            if not nombre or not tipo:
                resumen["errores"].append(f"Opción #{indice} sin nombre o tipo")
                continue

            id_opcion = combo_dao.guardar_opcion(id_combo, nombre, tipo)
            if not id_opcion:
                resumen["errores"].append(f"No se pudo guardar la opción #{indice}")
                continue

            resumen["opciones_creadas"] += 1
            valores = opcion.get("valores", [])
            if not isinstance(valores, list):
                resumen["errores"].append(f"Valores inválidos en opción #{indice}")
                continue

            for valor in valores:
                descripcion, costo_adicional = self._normalizar_valor_predefinido(valor)
                if not descripcion:
                    continue
                id_valor = combo_dao.guardar_valor(id_opcion, descripcion, costo_adicional)
                if id_valor:
                    resumen["valores_creados"] += 1
                else:
                    resumen["errores"].append(
                        f"No se pudo guardar un valor de la opción #{indice}"
                    )
        return resumen

    def guardar_combo(self, id_restaurante, nombre, descripcion, numero, precio, imagen=None, opciones_predefinidas=None):
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
                respuesta = {
                    "exito": True,
                    "mensaje": "Combo creado correctamente",
                    "id": id_nuevo,
                    "imagen_url": self._resolver_imagen_url(imagen),
                }
                if opciones_predefinidas:
                    respuesta["opciones_predefinidas"] = self._guardar_opciones_predefinidas(
                        id_nuevo,
                        opciones_predefinidas,
                    )
                return respuesta
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
                return {
                    "exito": True,
                    "mensaje": "Combo actualizado correctamente",
                    "imagen_url": self._resolver_imagen_url(imagen),
                }
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
            combos = [self._adjuntar_imagen_url(combo) for combo in combos]
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
