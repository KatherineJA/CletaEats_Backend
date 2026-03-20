from modelo.restaurante import Restaurante
from dao.restaurante_dao import RestauranteDAO

class RestauranteService:

    def __init__(self):
        self.restaurante_dao = RestauranteDAO()

    def registrar_restaurante(self, cedula_juridica, nombre, direccion, tipo_comida):
        # Verificar que la cédula jurídica no exista
        if self.restaurante_dao.buscar_por_cedula_juridica(cedula_juridica):
            return {"exito": False, "mensaje": "La cédula jurídica ya está registrada"}

        # Crear restaurante
        restaurante = Restaurante.nuevo(cedula_juridica, nombre, direccion, tipo_comida)
        guardado = self.restaurante_dao.guardar(restaurante)
        if not guardado:
            return {"exito": False, "mensaje": "Error al guardar restaurante"}

        return {"exito": True, "mensaje": "Restaurante registrado correctamente"}

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