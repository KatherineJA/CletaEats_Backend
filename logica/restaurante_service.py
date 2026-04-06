from modelo.restaurante import Restaurante
from dao.restaurante_dao import RestauranteDAO
from dao.combo_dao import ComboDAO


class RestauranteService:

    def __init__(self):
        self.restaurante_dao = RestauranteDAO()
        self.combo_dao = ComboDAO()

    def registrar_restaurante(self, cedula_juridica, nombre, direccion, tipo_comida):
        if self.restaurante_dao.buscar_por_cedula_juridica(cedula_juridica):
            return {"exito": False, "mensaje": "La cédula jurídica ya está registrada"}

        restaurante = Restaurante.nuevo(cedula_juridica, nombre, direccion, tipo_comida)
        guardado = self.restaurante_dao.guardar(restaurante)

        if not guardado:
            return {"exito": False, "mensaje": "Error al guardar restaurante"}

        try:
            for i in range(1, 10):
                precio_calculado = 4000.0 + ((i - 1) * 1000.0)
                self.combo_dao.guardar(guardado.get_id(), i, precio_calculado)

            return {"exito": True, "mensaje": "Restaurante y sus 9 combos creados correctamente"}
        except Exception as e:
            return {"exito": True, "mensaje": f"Restaurante creado, pero hubo un problema con los combos: {str(e)}"}

    def listar_restaurantes(self):
        restaurantes = self.restaurante_dao.listar_todos()
        resultado = []
        for r in restaurantes:
            resultado.append({
                "id": r.get_id(),
                "nombre": r.get_nombre(),
                "cedula_juridica": r.get_cedula_juridica(),
                "direccion": r.direccion,
                "tipo_comida": r.get_tipo_comida()
            })
        return {"exito": True, "restaurantes": resultado}

    def obtener_menu(self, restaurante_id):
        combos = self.combo_dao.listar_por_restaurante(restaurante_id)
        return {"exito": True, "combos": combos}