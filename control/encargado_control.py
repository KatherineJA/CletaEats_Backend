# encargado_control.py
from logica.encargado_service import EncargadoService
from logica.restaurante_service import RestauranteService  # <-- Corregido el import aquí

encargado_service = EncargadoService()
restaurante_service = RestauranteService()  # <-- Instanciamos el servicio aquí


def manejar_post(path, body, responder):
    if path == "/registro/encargado":
        campos = ["cedula", "nombre", "correo", "password", "telefono", "id_restaurante"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True

        # 1. Guardamos primero el diccionario que retorna el método en la variable 'resultado'
        resultado = encargado_service.registrar_encargado(
            body["cedula"], body["nombre"], body["correo"], body["password"],
            body["telefono"], body["id_restaurante"],
            body.get("latitud"), body.get("longitud")
        )

        # 2. Si el encargado se creó bien, hacemos la actualización cruzada en Restaurante
        if resultado.get("exito"):
            id_usuario_creado = resultado.get("id")  # El ID autogenerado del nuevo encargado
            id_restaurante_existente = body["id_restaurante"]

            # Ejecutamos la actualización en la tabla Restaurante
            restaurante_service.asociar_encargado_a_restaurante(id_restaurante_existente, id_usuario_creado)

        # 3. Respondemos al frontend una única vez al puro final del flujo
        responder(200, resultado)
        return True

    elif path == "/combo":
        campos = ["id_usuario", "nombre", "descripcion", "numero"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, encargado_service.agregar_combo(
            body["id_usuario"], body["nombre"], body["descripcion"],
            body["numero"], body.get("imagen")
        ))
        return True

    elif path == "/combo/opcion":
        campos = ["id_combo", "nombre", "tipo"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, encargado_service.agregar_opcion_combo(
            body["id_combo"], body["nombre"], body["tipo"]
        ))
        return True

    elif path == "/combo/opcion/valor":
        campos = ["id_opcion", "descripcion"]
        if not all(body.get(c) for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos"})
            return True
        responder(200, encargado_service.agregar_valor_opcion(
            body["id_opcion"], body["descripcion"], body.get("costo_adicional", 0)
        ))
        return True

    return False


def manejar_get(path, query, responder):
    if path == "/combo/mis-combos":
        id_usuario = query.get("id", [None])[0]
        if not id_usuario:
            responder(400, {"exito": False, "mensaje": "ID de usuario requerido"})
            return True
        responder(200, encargado_service.listar_combos(id_usuario))
        return True

    return False


def obtener_kpis_principales(self):
    return {
        "exito": True,
        "datos": {
            "total_ventas": self.reporte_dao.monto_total_global(),
            "hora_pico": self.reporte_dao.hora_pico(),
            "cliente_top": self.reporte_dao.cliente_mas_pedidos(),
            "restaurante_top": self.reporte_dao.restaurante_mas_pedidos()
        }
    }