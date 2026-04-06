class Repartidor:
    def __init__(self):
        self.id = None
        self.usuario_id = None # <--- Vinculado a tu tabla
        self.cedula = ""
        self.nombre = ""
        self.correo = ""
        self.direccion = ""
        self.telefono = ""
        self.tarjeta = ""
        self.estado = "disponible"
        self.amonestaciones = 0
        self.km_diarios = 0.0

    @classmethod
    def nuevo(cls, usuario_id, cedula, nombre, correo, direccion, telefono, tarjeta):
        rep = cls()
        rep.usuario_id = usuario_id
        rep.cedula = cedula
        rep.nombre = nombre
        rep.correo = correo
        rep.direccion = direccion
        rep.telefono = telefono
        rep.tarjeta = tarjeta
        return rep

    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def get_cedula(self): return self.cedula
    def get_nombre(self): return self.nombre
    def get_correo(self): return self.correo
    def get_direccion(self): return self.direccion
    def get_telefono(self): return self.telefono
    def get_tarjeta(self): return self.tarjeta
    def get_estado(self): return self.estado
    def set_estado(self, estado): self.estado = estado
