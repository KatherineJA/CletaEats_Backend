import bcrypt

class Usuario:

    # Constructor default
    def __init__(self):
        self.id = None
        self.correo = ""
        self.password_hash = ""
        self.rol = ""

    # Constructor sobrecargado
    @classmethod
    def nuevo(cls, correo, password, rol):
        u = cls()
        u.correo = correo
        u.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        u.rol = rol
        return u

    # Getters y setters
    def get_id(self): return self.id
    def set_id(self, id): self.id = id

    def get_correo(self): return self.correo
    def set_correo(self, correo): self.correo = correo

    def get_rol(self): return self.rol
    def set_rol(self, rol): self.rol = rol


    def verificar_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __str__(self):
        return f"Usuario[id={self.id}, correo={self.correo}, rol={self.rol}]"