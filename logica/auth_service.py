from modelo.usuario import Usuario
from modelo.cliente import Cliente
from modelo.repartidor import Repartidor
from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from dao.repartidor_dao import RepartidorDAO


class AuthService:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.cliente_dao = ClienteDAO()
        self.repartidor_dao = RepartidorDAO()

    def registrar_cliente(self, cedula, nombre, correo, password, telefono, numero_tarjeta, latitud=None, longitud=None):
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya está registrado"}

        if self.usuario_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cédula ya está registrada"}

        usuario = Usuario.nuevo(cedula, nombre, correo, password, telefono, "CLIENTE", latitud, longitud)
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        cliente = Cliente.nuevo(usuario_guardado.get_id(), numero_tarjeta)
        if not self.cliente_dao.guardar(cliente):
            return {"exito": False, "mensaje": "Error al crear cliente"}

        return {"exito": True, "mensaje": "Cliente registrado correctamente", "id": usuario_guardado.get_id()}

    def registrar_repartidor(self, cedula, nombre, correo, password, telefono, numero_tarjeta, latitud=None, longitud=None):
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya está registrado"}

        if self.usuario_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cédula ya está registrada"}

        usuario = Usuario.nuevo(cedula, nombre, correo, password, telefono, "REPARTIDOR", latitud, longitud)
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        repartidor = Repartidor.nuevo(usuario_guardado.get_id(), numero_tarjeta)
        if not self.repartidor_dao.guardar(repartidor):
            return {"exito": False, "mensaje": "Error al crear repartidor"}

        return {"exito": True, "mensaje": "Repartidor registrado correctamente", "id": usuario_guardado.get_id()}

    def login(self, correo, password):
        usuario = self.usuario_dao.buscar_por_correo(correo)
        if not usuario:
            return {"exito": False, "mensaje": "Correo o contraseña incorrectos"}

        if not usuario.verificar_password(password):
            return {"exito": False, "mensaje": "Correo o contraseña incorrectos"}

        if usuario.get_rol() == "CLIENTE":
            cliente = self.cliente_dao.buscar_por_id(usuario.get_id())
            if cliente and not cliente.esta_activo():
                return {"exito": False, "mensaje": "Tu cuenta está suspendida. Contactá al administrador."}

        if usuario.get_rol() == "REPARTIDOR":
            repartidor = self.repartidor_dao.buscar_por_id(usuario.get_id())
            if repartidor and repartidor.estado == "SUSPENDIDO":
                return {"exito": False, "mensaje": "Tu cuenta está suspendida. Contactá al administrador."}

        return {
            "exito": True,
            "mensaje": "Login exitoso",
            "id": usuario.get_id(),
            "nombre": usuario.nombre,
            "rol": usuario.get_rol()
        }