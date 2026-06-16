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
    if path == "/restaurante/actualizar":
        id_res = body.get("id_restaurante")
        if not id_res:
            responder(400, {"exito": False, "mensaje": "id_restaurante es requerido"})
            return True

        # Imagen: puede venir como archivo o como string (URL existente)
        imagen_raw = body.get("imagen")
        if isinstance(imagen_raw, dict):
            imagen_url, error = _guardar_imagen_restaurante(imagen_raw)
            if error:
                responder(400, {"exito": False, "mensaje": error})
                return True
        elif isinstance(imagen_raw, str) and imagen_raw.strip():
            imagen_url = imagen_raw.strip()
        else:
            imagen_url = None  # no actualiza imagen si no viene

        resultado = restaurante_service.actualizar_restaurante(
            id_restaurante=int(id_res),
            nombre=body.get("nombre"),
            direccion=body.get("direccion"),
            tipo_comida=body.get("tipo_comida"),
            imagen=imagen_url
        )
        responder(200, resultado)
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
CARPETA_IMAGENES_RESTAURANTES = os.path.join("uploads", "restaurantes")

def _guardar_imagen_restaurante(imagen):
    if not isinstance(imagen, dict):
        return None, "Formato de imagen inválido"
    data = imagen.get("data")
    if not isinstance(data, (bytes, bytearray)) or not data:
        return None, "Imagen vacía"

    tipo = _detectar_tipo_imagen(data)  # reutilizás la misma función
    if tipo not in TIPOS_IMAGEN_PERMITIDOS:
        return None, "Tipo de imagen no permitido"

    usar_imgbb = os.environ.get("USAR_IMGBB", "false").lower() == "true"
    if usar_imgbb:
        try:
            import base64, requests
            foto_b64 = base64.b64encode(data).decode("utf-8")
            response = requests.post("https://api.imgbb.com/1/upload",
                data={"key": os.environ.get("IMGBB_API_KEY", ""), "image": foto_b64})
            resultado = response.json()
            if resultado.get("success"):
                return resultado["data"]["url"], None
            return None, "Error al subir a ImgBB"
        except Exception as e:
            return None, f"Error ImgBB: {str(e)}"

    os.makedirs(CARPETA_IMAGENES_RESTAURANTES, exist_ok=True)
    ext = TIPOS_IMAGEN_PERMITIDOS[tipo]
    nombre_archivo = f"restaurante_{uuid.uuid4().hex}.{ext}"
    ruta = os.path.join(CARPETA_IMAGENES_RESTAURANTES, nombre_archivo)
    with open(ruta, "wb") as f:
        f.write(data)
    return f"/{CARPETA_IMAGENES_RESTAURANTES.replace(os.sep, '/')}/{nombre_archivo}", None