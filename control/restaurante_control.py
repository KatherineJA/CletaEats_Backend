from logica.restaurante_service import RestauranteService
from logica.encargado_service import EncargadoService  # <-- Importamos el servicio de encargados

restaurante_service = RestauranteService()
encargado_service = EncargadoService()  # <-- Lo instanciamos


def manejar_post(path, body, responder):
    # RUTA A: Crear de forma UNIFICADA (Restaurante + Encargado nuevo a la vez)
    if path == "/restaurantes/registrar-con-encargado":
        campos_restaurante = ["nombre_restaurante", "cedula_juridica", "direccion", "tipo_comida"]
        if not all(body.get(c) for c in campos_restaurante):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos del restaurante"})
            return True

        encargado_data = body.get("encargado", {})
        campos_encargado = ["cedula", "nombre_completo", "correo", "password", "telefono"]
        if not all(encargado_data.get(c) for c in campos_encargado):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos del encargado"})
            return True

        try:
            # 1. Registrar el restaurante inicialmente sin encargado (None)
            resultado_restaurante = restaurante_service.registrar_restaurante(
                body["nombre_restaurante"],
                body["cedula_juridica"],
                body["direccion"],
                body["tipo_comida"],
                body.get("latitud"),
                body.get("longitud"),
                None
            )

            if not resultado_restaurante.get("exito"):
                responder(400, {"exito": False,
                                "mensaje": resultado_restaurante.get("mensaje", "No se pudo registrar el restaurante")})
                return True

            id_restaurante_creado = resultado_restaurante.get("id")

            # 2. Registrar al Encargado usando el servicio correspondiente
            resultado_encargado = encargado_service.registrar_encargado(
                encargado_data["cedula"],
                encargado_data["nombre_completo"],
                encargado_data["correo"],
                encargado_data["password"],
                encargado_data["telefono"],
                id_restaurante_creado,
                body.get("latitud"),
                body.get("longitud")
            )

            if not resultado_encargado.get("exito"):
                responder(400, {"exito": False, "mensaje": resultado_encargado.get("mensaje",
                                                                                   "Restaurante creado, pero no se pudo registrar el encargado")})
                return True

            # 3. ¡VINCULACIÓN BIDIRECCIONAL REQUERIDA POR TU BD!
            # Como el restaurante se creó con encargado=None, ahora que tienes el ID del encargado
            # debes actualizar la tabla Restaurante. Asegúrate de tener este método en tu service o DAO:
            id_usuario_encargado = resultado_encargado.get("id")
            restaurante_service.asociar_encargado_a_restaurante(id_restaurante_creado, id_usuario_encargado)

            responder(200, {"exito": True, "mensaje": "¡Restaurante y encargado creados y vinculados con éxito!"})
            return True

        except Exception as e:
            responder(500, {"exito": False, "mensaje": f"Error interno en el servidor: {str(e)}"})
            return True

    # RUTA B: Crear SOLO el restaurante (El encargado se asignará después)
    if path == "/restaurante":
        campos = ["nombre", "cedula_juridica", "direccion", "tipo_comida"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos del restaurante"})
            return True

        # Si body.get("id_encargado") no se envía, pasará como None a la base de datos (id_encargado INT NULL)
        responder(200, restaurante_service.registrar_restaurante(
            body["nombre"], body["cedula_juridica"], body["direccion"], body["tipo_comida"],
            body.get("latitud"), body.get("longitud"), body.get("id_encargado")
        ))
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/restaurantes":
        responder(200, restaurante_service.listar_restaurantes())
        return True

    elif path == "/restaurantes/menu":
        id_res = query.get("id", [None])[0]
        if not id_res:
            responder(400, {"exito": False, "mensaje": "ID de restaurante requerido"})
            return True
        responder(200, restaurante_service.obtener_menu(id_res))
        return True

    return False