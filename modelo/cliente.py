class Cliente:

    # Constructor default
    def __init__(self):
        self.id = None
        self.usuario_id = None
        self.cedula = ""
        self.nombre = ""
        self.direccion = ""
        self.tarjeta = ""
        self.telefono = ""
        self.correo = ""
        self.estado = "activo"

    # Constructor sobrecargado
    @classmethod
    def nuevo(cls, usuario_id, cedula, nombre, direccion, tarjeta, telefono, correo):
        c = cls()
        c.usuario_id = usuario_id
        c.cedula = cedula
        c.nombre = nombre
        c.direccion = direccion
        c.tarjeta = tarjeta
        c.telefono = telefono
        c.correo = correo
        c.estado = "activo"
        return c

    # Getters y setters
    def get_id(self): return self.id
    def set_id(self, id): self.id = id

    def get_cedula(self): return self.cedula
    def set_cedula(self, cedula): self.cedula = cedula

    def get_nombre(self): return self.nombre
    def set_nombre(self, nombre): self.nombre = nombre

    def get_estado(self): return self.estado
    def set_estado(self, estado): self.estado = estado

    # Métodos de cálculo
    def esta_activo(self):
        return self.estado == "activo"

    def suspender(self):
        self.estado = "suspendido"

    def activar(self):
        self.estado = "activo"

    def __str__(self):
        return f"Cliente[id={self.id}, cedula={self.cedula}, nombre={self.nombre}, estado={self.estado}]"