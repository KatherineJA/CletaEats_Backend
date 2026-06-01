from logica.combo_service import ComboService

combo_service = ComboService()


def manejar_post(path, body, responder):
    # Asegurar que el cuerpo no sea None
    if body is None:
        body = {}

    # RUTA A: Crear un combo nuevo para un restaurante
    if path == "/combo":
        # 1. Recuperar los valores con tolerancia a tipos
        id_res_raw = body.get("id_restaurante")
        nombre_raw = body.get("nombre")
        precio_raw = body.get("precio")
        numero_raw = body.get("numero")

        # 2. Diagnóstico claro de campos faltantes para evitar respuestas genéricas
        if id_res_raw is None or str(id_res_raw).strip() == "":
            responder(400, {"exito": False, "mensaje": "Falta el campo requerido: id_restaurante"})
            return True

        if nombre_raw is None or str(nombre_raw).strip() == "":
            responder(400, {"exito": False, "mensaje": "Falta el campo requerido: nombre"})
            return True

        if precio_raw is None or str(precio_raw).strip() == "":
            responder(400, {"exito": False, "mensaje": "Falta el campo requerido: precio"})
            return True

        # 3. Procesar y Castear de forma segura
        try:
            id_restaurante = int(id_res_raw)
            nombre = str(nombre_raw).strip()
            precio = float(precio_raw)

            # Manejar el número de combo de forma segura
            if numero_raw is None or str(numero_raw).strip() == "":
                numero = 0
            else:
                numero = int(numero_raw)

        except (ValueError, TypeError) as e:
            responder(400, {
                "exito": False,
                "mensaje": f"Error de formato numérico en el backend al procesar id_restaurante, precio o número: {str(e)}"
            })
            return True

        # 4. Enviar al Servicio
        try:
            resultado = combo_service.guardar_combo(
                id_restaurante=id_restaurante,
                nombre=nombre,
                descripcion=str(body.get("descripcion", "")).strip(),
                numero=numero,
                precio=precio,
                imagen=body.get("imagen", None)
            )

            if not resultado or not resultado.get("exito"):
                responder(400, resultado if resultado else {"exito": False, "mensaje": "No se pudo guardar el combo en base de datos"})
            else:
                responder(200, resultado)

        except Exception as e:
            responder(500, {"exito": False, "mensaje": f"Error crítico en ComboService: {str(e)}"})
        return True

    # RUTA B: Actualizar un combo existente
    if path == "/combo/actualizar":
        campos = ["id_combo", "nombre", "numero", "precio"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos en actualización: id_combo, nombre, numero, precio"})
            return True

        resultado = combo_service.actualizar_combo(
            id_combo=body["id_combo"],
            nombre=body["nombre"],
            descripcion=body.get("descripcion", ""),
            numero=body["numero"],
            precio=body["precio"],
            imagen=body.get("imagen", None)
        )
        responder(200, resultado)
        return True

    # RUTA C: Eliminar un combo
    if path == "/combo/eliminar":
        if not body.get("id_combo"):
            responder(400, {"exito": False, "mensaje": "id_combo es requerido para eliminar"})
            return True

        resultado = combo_service.eliminar_combo(body["id_combo"])
        responder(200, resultado)
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/combos":
        id_restaurante = query.get("id_restaurante", [None])[0]
        if not id_restaurante:
            responder(400, {"exito": False, "mensaje": "id_restaurante es requerido"})
            return True

        responder(200, combo_service.listar_combos(id_restaurante))
        return True

    if path == "/combo/detalle":
        id_combo = query.get("id", [None])[0]
        if not id_combo:
            responder(400, {"exito": False, "mensaje": "id del combo es requerido"})
            return True

        responder(200, combo_service.detalle_combo(id_combo))
        return True

    return False