from logica.combo_service import ComboService
import json
import os
import uuid

combo_service = ComboService()

CARPETA_IMAGENES_COMBOS = os.path.join("uploads", "combos")
TIPOS_IMAGEN_PERMITIDOS = {
    "jpeg": "jpg",
    "png": "png",
    "gif": "gif",
    "webp": "webp",
}


def _detectar_tipo_imagen(data):
    if len(data) >= 3 and data[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if len(data) >= 6 and data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None


def _guardar_archivo_imagen(imagen):
    if not isinstance(imagen, dict):
        return None, "El campo imagen no tiene un formato de archivo válido"

    data = imagen.get("data")
    if not isinstance(data, (bytes, bytearray)) or not data:
        return None, "El archivo imagen está vacío"

    tipo_detectado = _detectar_tipo_imagen(data)
    if tipo_detectado not in TIPOS_IMAGEN_PERMITIDOS:
        return None, "El archivo enviado no es una imagen válida (jpg, png, gif o webp)"

    # Si está configurado para usar ImgBB (u otro servicio vía env), subir ahí y devolver URL
    usar_imgbb = os.environ.get("USAR_IMGBB", "false").lower() == "true"
    if usar_imgbb:
        try:
            import base64
            import requests
            IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY", "")
            foto_b64 = base64.b64encode(data).decode("utf-8")
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                data={"key": IMGBB_API_KEY, "image": foto_b64}
            )
            resultado = response.json()
            if resultado.get("success"):
                url = resultado["data"]["url"]
                return url, None
            return None, "Error al subir imagen a ImgBB"
        except Exception as e:
            return None, f"Error al subir imagen a ImgBB: {str(e)}"

    # Fallback: guardar en disco y devolver ruta relativa
    os.makedirs(CARPETA_IMAGENES_COMBOS, exist_ok=True)
    extension = TIPOS_IMAGEN_PERMITIDOS[tipo_detectado]
    nombre_archivo = f"combo_{uuid.uuid4().hex}.{extension}"
    ruta_archivo = os.path.join(CARPETA_IMAGENES_COMBOS, nombre_archivo)

    with open(ruta_archivo, "wb") as archivo:
        archivo.write(data)

    return f"/{CARPETA_IMAGENES_COMBOS.replace(os.sep, '/')}/{nombre_archivo}", None


def _extraer_imagen(body):
    imagen = body.get("imagen")
    if imagen in (None, ""):
        return None, None

    if isinstance(imagen, str):
        return imagen.strip(), None

    return _guardar_archivo_imagen(imagen)


def _parsear_opciones_predefinidas(raw):
    if raw in (None, ""):
        return None, None

    if isinstance(raw, list):
        return raw, None

    if isinstance(raw, str):
        try:
            opciones = json.loads(raw)
        except json.JSONDecodeError:
            return None, "opciones_predefinidas debe venir como JSON válido"

        if not isinstance(opciones, list):
            return None, "opciones_predefinidas debe ser un arreglo JSON"
        return opciones, None

    return None, "Formato inválido para opciones_predefinidas"


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

        imagen_url, error_imagen = _extraer_imagen(body)
        if error_imagen:
            responder(400, {"exito": False, "mensaje": error_imagen})
            return True

        opciones_predefinidas, error_opciones = _parsear_opciones_predefinidas(body.get("opciones_predefinidas"))
        if error_opciones:
            responder(400, {"exito": False, "mensaje": error_opciones})
            return True

        # 4. Enviar al Servicio
        try:
            resultado = combo_service.guardar_combo(
                id_restaurante=id_restaurante,
                nombre=nombre,
                descripcion=str(body.get("descripcion", "")).strip(),
                numero=numero,
                precio=precio,
                imagen=imagen_url,
                opciones_predefinidas=opciones_predefinidas,
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

        imagen_url, error_imagen = _extraer_imagen(body)
        if error_imagen:
            responder(400, {"exito": False, "mensaje": error_imagen})
            return True

        resultado = combo_service.actualizar_combo(
            id_combo=body["id_combo"],
            nombre=body["nombre"],
            descripcion=body.get("descripcion", ""),
            numero=body["numero"],
            precio=body["precio"],
            imagen=imagen_url,
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

    if path == "/combo/opcion":
        campos = ["id_combo", "nombre", "tipo"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos: id_combo, nombre, tipo"})
            return True

        responder(200, combo_service.agregar_opcion_combo(
            body["id_combo"], body["nombre"], body["tipo"]
        ))
        return True

    if path == "/combo/opcion/actualizar":
        campos = ["id_opcion", "nombre", "tipo"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos: id_opcion, nombre, tipo"})
            return True

        responder(200, combo_service.actualizar_opcion_combo(
            body["id_opcion"], body["nombre"], body["tipo"]
        ))
        return True

    if path == "/combo/opcion/eliminar":
        if body.get("id_opcion") is None:
            responder(400, {"exito": False, "mensaje": "id_opcion es requerido para eliminar"})
            return True

        responder(200, combo_service.eliminar_opcion_combo(body["id_opcion"]))
        return True

    if path == "/combo/opcion/valor":
        campos = ["id_opcion", "descripcion"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos: id_opcion, descripcion"})
            return True

        responder(200, combo_service.agregar_valor_opcion(
            body["id_opcion"], body["descripcion"], body.get("costo_adicional", 0)
        ))
        return True

    if path == "/combo/opcion/valor/actualizar":
        campos = ["id_valor", "descripcion"]
        if not all(body.get(c) is not None for c in campos):
            responder(400, {"exito": False, "mensaje": "Faltan campos requeridos: id_valor, descripcion"})
            return True

        responder(200, combo_service.actualizar_valor_opcion(
            body["id_valor"], body["descripcion"], body.get("costo_adicional", 0)
        ))
        return True

    if path == "/combo/opcion/valor/eliminar":
        if body.get("id_valor") is None:
            responder(400, {"exito": False, "mensaje": "id_valor es requerido para eliminar"})
            return True

        responder(200, combo_service.eliminar_valor_opcion(body["id_valor"]))
        return True

    return False


def manejar_get(path, query, responder):
    def obtener_id(*nombres):
        for nombre in nombres:
            valor = query.get(nombre, [None])[0]
            if valor not in (None, ""):
                return valor
        return None

    if path == "/combos":
        id_restaurante = query.get("id_restaurante", [None])[0]
        if not id_restaurante:
            responder(400, {"exito": False, "mensaje": "id_restaurante es requerido"})
            return True

        responder(200, combo_service.listar_combos(id_restaurante))
        return True

    if path == "/combo/detalle":
        id_combo = obtener_id("id", "id_combo")
        if not id_combo:
            responder(400, {"exito": False, "mensaje": "id del combo es requerido"})
            return True

        responder(200, combo_service.detalle_combo(id_combo))
        return True

    if path == "/combo/opciones":
        id_combo = obtener_id("id", "id_combo")
        if not id_combo:
            responder(400, {"exito": False, "mensaje": "id del combo es requerido"})
            return True

        responder(200, combo_service.listar_opciones(id_combo))
        return True

    if path == "/combo/opcion/valores":
        id_opcion = obtener_id("id", "id_opcion")
        if not id_opcion:
            responder(400, {"exito": False, "mensaje": "id de la opción es requerido"})
            return True

        responder(200, combo_service.listar_valores_opcion(id_opcion))
        return True

    return False