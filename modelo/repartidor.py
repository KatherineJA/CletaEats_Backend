class Repartidor:

    def __init__(self):
        self.id_usuario = None
        self.numero_tarjeta = ""
        self.estado = "DISPONIBLE"  # DISPONIBLE / OCUPADO / SUSPENDIDO
        self.kilometros_diarios = 0.0

    @classmethod
    def nuevo(cls, id_usuario, numero_tarjeta):
        r = cls()
        r.id_usuario = id_usuario
        r.numero_tarjeta = numero_tarjeta
        return r

    def get_id_usuario(self): return self.id_usuario
    def get_estado(self): return self.estado
    def set_estado(self, estado): self.estado = estado

    def esta_disponible(self): return self.estado == "DISPONIBLE"

    def __str__(self):
        return f"Repartidor[id_usuario={self.id_usuario}, estado={self.estado}]"