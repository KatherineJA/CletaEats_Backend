import bcrypt

class Usuario:

    def __init__(self):
        self.id = None
        self.cedula = ""
        self.nombre = ""
        self.correo = ""
        self.contrasena = ""
        self.telefono = ""
        self.rol = ""       # ADMIN / CLIENTE / REPARTIDOR / ENCARGADO
        self.latitud = None
        self.longitud = None

    @classmethod
    def nuevo(cls, cedula, nombre, correo, password, telefono, rol, latitud=None, longitud=None):
        u = cls()
        u.cedula = cedula
        u.nombre = nombre
        u.correo = correo
        u.contrasena = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        u.telefono = telefono
        u.rol = rol
        u.latitud = latitud
        u.longitud = longitud
        return u

    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def get_correo(self): return self.correo
    def get_rol(self): return self.rol

    def verificar_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.contrasena.encode('utf-8')
        )

    def __str__(self):
        return f"Usuario[id={self.id}, correo={self.correo}, rol={self.rol}]"