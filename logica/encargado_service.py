from dao.encargado_dao import EncargadoDAO
from dao.combo_dao import ComboDAO
from dao.usuario_dao import UsuarioDAO
from dao.restaurante_dao import RestauranteDAO
from modelo.usuario import Usuario


class EncargadoService:

    def __init__(self):
        self.encargado_dao = EncargadoDAO()
        self.combo_dao = ComboDAO()
        self.usuario_dao = UsuarioDAO()
        self.restaurante_dao = RestauranteDAO()

    def registrar_encargado(self, cedula, nombre, correo, password, telefono, id_restaurante,
                             latitud=None, longitud=None):
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya está registrado"}

        if self.usuario_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cédula ya está registrada"}

        restaurante = self.restaurante_dao.buscar_por_id(id_restaurante)
        if not restaurante:
            return {"exito": False, "mensaje": "El restaurante indicado no existe"}

        usuario = Usuario.nuevo(cedula, nombre, correo, password, telefono, "ENCARGADO", latitud, longitud)
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        ok = self.encargado_dao.guardar(usuario_guardado.get_id(), id_restaurante)
        if not ok:
            return {"exito": False, "mensaje": "Error al asignar encargado al restaurante"}

        return {"exito": True, "mensaje": "Encargado registrado correctamente", "id": usuario_guardado.get_id()}

    def agregar_combo(self, id_usuario, nombre, descripcion, numero, imagen=None):
        id_restaurante = self.encargado_dao.buscar_restaurante_de_encargado(id_usuario)
        if not id_restaurante:
            return {"exito": False, "mensaje": "No tenés un restaurante asignado"}

        if not (1 <= numero <= 9):
            return {"exito": False, "mensaje": "El número de combo debe estar entre 1 y 9"}

        precio = 4000 + (numero - 1) * 1000

        combo = {
            "id_restaurante": id_restaurante,
            "nombre": nombre,
            "descripcion": descripcion,
            "numero": numero,
            "precio": precio,
            "imagen": imagen
        }

        id_combo = self.combo_dao.guardar(combo)
        if not id_combo:
            return {"exito": False, "mensaje": "Error al guardar el combo"}

        return {"exito": True, "mensaje": "Combo agregado correctamente", "id_combo": id_combo, "precio": precio}

    def agregar_opcion_combo(self, id_combo, nombre, tipo):
        tipos_validos = ["SELECCION_UNICA", "MULTIPLE", "BOOLEANO"]
        if tipo not in tipos_validos:
            return {"exito": False, "mensaje": f"Tipo inválido. Opciones: {tipos_validos}"}

        id_opcion = self.combo_dao.guardar_opcion(id_combo, nombre, tipo)
        if not id_opcion:
            return {"exito": False, "mensaje": "Error al guardar la opción"}

        return {"exito": True, "mensaje": "Opción agregada", "id_opcion": id_opcion}

    def agregar_valor_opcion(self, id_opcion, descripcion, costo_adicional=0):
        id_valor = self.combo_dao.guardar_valor_opcion(id_opcion, descripcion, costo_adicional)
        if not id_valor:
            return {"exito": False, "mensaje": "Error al guardar el valor"}

        return {"exito": True, "mensaje": "Valor agregado", "id_valor": id_valor}

    def listar_combos(self, id_usuario):
        id_restaurante = self.encargado_dao.buscar_restaurante_de_encargado(id_usuario)
        if not id_restaurante:
            return {"exito": False, "mensaje": "No tenés un restaurante asignado"}

        combos = self.combo_dao.listar_por_restaurante(id_restaurante)
        for combo in combos:
            combo['opciones'] = self.combo_dao.listar_opciones_por_combo(combo['id'])
        return {"exito": True, "datos": combos}