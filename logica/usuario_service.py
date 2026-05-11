from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from dao.repartidor_dao import RepartidorDAO


class UsuarioService:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.cliente_dao = ClienteDAO()
        self.repartidor_dao = RepartidorDAO()

    def obtener_perfil(self, id_usuario):
        usuario = self.usuario_dao.buscar_por_id(id_usuario)
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado"}
        return {
            "exito": True,
            "datos": {
                "id": usuario.id,
                "cedula": usuario.cedula,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "telefono": usuario.telefono,
                "rol": usuario.rol,
                "latitud": usuario.latitud,
                "longitud": usuario.longitud
            }
        }

    def editar_perfil(self, id_usuario, telefono, nombre=None, latitud=None, longitud=None):
        if not telefono:
            return {"exito": False, "mensaje": "El teléfono es requerido"}
        ok = self.usuario_dao.actualizar_perfil(id_usuario, telefono, latitud, longitud)
        if ok and nombre:
            self.usuario_dao.actualizar_nombre(id_usuario, nombre)
        return {"exito": ok, "mensaje": "Perfil actualizado" if ok else "Error al actualizar perfil"}

    def editar_tarjeta_cliente(self, id_usuario, numero_tarjeta):
        if not numero_tarjeta:
            return {"exito": False, "mensaje": "El número de tarjeta es requerido"}
        ok = self.usuario_dao.actualizar_tarjeta_cliente(id_usuario, numero_tarjeta)
        return {"exito": ok, "mensaje": "Tarjeta actualizada" if ok else "Error al actualizar tarjeta"}

    def editar_tarjeta_repartidor(self, id_usuario, numero_tarjeta):
        if not numero_tarjeta:
            return {"exito": False, "mensaje": "El número de tarjeta es requerido"}
        ok = self.usuario_dao.actualizar_tarjeta_repartidor(id_usuario, numero_tarjeta)
        return {"exito": ok, "mensaje": "Tarjeta actualizada" if ok else "Error al actualizar tarjeta"}

    # ------------------------------------------------------------------
    # Reactivación manual por el administrador
    # ------------------------------------------------------------------
    def reactivar_cliente(self, id_usuario):
        usuario = self.usuario_dao.buscar_por_id(id_usuario)
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado"}
        if usuario.rol != "CLIENTE":
            return {"exito": False, "mensaje": "El usuario no es un cliente"}

        cliente = self.cliente_dao.buscar_por_id(id_usuario)
        if not cliente:
            return {"exito": False, "mensaje": "Cliente no encontrado"}
        if cliente.esta_activo():
            return {"exito": False, "mensaje": "El cliente ya está activo"}

        ok = self.cliente_dao.actualizar_estado(id_usuario, "ACTIVO")
        return {"exito": ok, "mensaje": "Cliente reactivado correctamente" if ok else "Error al reactivar"}

    def reactivar_repartidor(self, id_usuario):
        usuario = self.usuario_dao.buscar_por_id(id_usuario)
        if not usuario:
            return {"exito": False, "mensaje": "Usuario no encontrado"}
        if usuario.rol != "REPARTIDOR":
            return {"exito": False, "mensaje": "El usuario no es un repartidor"}

        repartidor = self.repartidor_dao.buscar_por_id(id_usuario)
        if not repartidor:
            return {"exito": False, "mensaje": "Repartidor no encontrado"}
        if repartidor.get_estado() != "SUSPENDIDO":
            return {"exito": False, "mensaje": "El repartidor no está suspendido"}

        ok = self.repartidor_dao.actualizar_estado(id_usuario, "DISPONIBLE")
        return {"exito": ok, "mensaje": "Repartidor reactivado correctamente" if ok else "Error al reactivar"}