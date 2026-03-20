from modelo.usuario import Usuario
from modelo.cliente import Cliente
from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO

class AuthService:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.cliente_dao = ClienteDAO()

    def registrar_cliente(self, correo, password, cedula, nombre, direccion, tarjeta, telefono):
        # Verificar que el correo no exista
        if self.usuario_dao.buscar_por_correo(correo):
            return {"exito": False, "mensaje": "El correo ya está registrado"}

        # Verificar que la cédula no exista
        if self.cliente_dao.buscar_por_cedula(cedula):
            return {"exito": False, "mensaje": "La cédula ya está registrada"}

        # Crear usuario
        usuario = Usuario.nuevo(correo, password, "cliente")
        usuario_guardado = self.usuario_dao.guardar(usuario)
        if not usuario_guardado:
            return {"exito": False, "mensaje": "Error al crear usuario"}

        # Crear cliente
        cliente = Cliente.nuevo(usuario_guardado.get_id(), cedula, nombre, direccion, tarjeta, telefono, correo)
        cliente_guardado = self.cliente_dao.guardar(cliente)
        if not cliente_guardado:
            return {"exito": False, "mensaje": "Error al crear cliente"}

        return {"exito": True, "mensaje": "Cliente registrado correctamente"}

    def login(self, correo, password):
        # Buscar usuario por correo
        usuario = self.usuario_dao.buscar_por_correo(correo)
        if not usuario:
            return {"exito": False, "mensaje": "Correo o contraseña incorrectos"}

        # Verificar contraseña
        if not usuario.verificar_password(password):
            return {"exito": False, "mensaje": "Correo o contraseña incorrectos"}

        return {
            "exito": True,
            "mensaje": "Login exitoso",
            "rol": usuario.get_rol(),
            "id": usuario.get_id()
        }