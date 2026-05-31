from dao.restaurante_dao import RestauranteDAO
from dao.combo_dao import ComboDAO
from modelo.restaurante import Restaurante


class RestauranteService:

    def __init__(self):
        self.restaurante_dao = RestauranteDAO()
        self.combo_dao = ComboDAO()

    def registrar_restaurante(self, nombre, cedula_juridica, direccion, tipo_comida, latitud=None, longitud=None, id_encargado=None):
        if self.restaurante_dao.buscar_por_cedula_juridica(cedula_juridica):
            return {"exito": False, "mensaje": "Ya existe un restaurante con esa cédula jurídica"}

        restaurante = Restaurante.nuevo(nombre, cedula_juridica, direccion, tipo_comida, latitud, longitud, id_encargado)
        resultado = self.restaurante_dao.guardar(restaurante)
        if not resultado:
            return {"exito": False, "mensaje": "Error al registrar restaurante"}

        return {"exito": True, "mensaje": "Restaurante registrado correctamente", "id": resultado.get_id()}

    def listar_restaurantes(self):
        restaurantes = self.restaurante_dao.listar_todos()
        return {"exito": True, "datos": restaurantes}

    def obtener_menu(self, id_restaurante):
        restaurante = self.restaurante_dao.buscar_por_id(id_restaurante)
        if not restaurante:
            return {"exito": False, "mensaje": "Restaurante no encontrado"}

        combos = self.combo_dao.listar_por_restaurante(id_restaurante)
        for combo in combos:
            combo['opciones'] = self.combo_dao.listar_opciones_por_combo(combo['id'])

        return {"exito": True, "restaurante": restaurante, "combos": combos}

    def asociar_encargado_a_restaurante(self, id_restaurante, id_encargado):
        """
        Vincula un encargado existente a un restaurante en la base de datos.
        """
        if not id_restaurante or not id_encargado:
            return {"exito": False, "mensaje": "ID de restaurante e ID de encargado son requeridos"}

        ok = self.restaurante_dao.actualizar_encargado(id_restaurante, id_encargado)
        return {
            "exito": ok,
            "mensaje": "Encargado asignado al restaurante con éxito" if ok else "Error al asociar el encargado en la base de datos"
        }