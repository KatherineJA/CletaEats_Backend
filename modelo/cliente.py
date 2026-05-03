class Cliente:

    def __init__(self):
        self.id_usuario = None
        self.numero_tarjeta = ""
        self.estado = "ACTIVO"  # ACTIVO / SUSPENDIDO

    @classmethod
    def nuevo(cls, id_usuario, numero_tarjeta):
        c = cls()
        c.id_usuario = id_usuario
        c.numero_tarjeta = numero_tarjeta
        return c

    def get_id_usuario(self): return self.id_usuario
    def get_estado(self): return self.estado
    def set_estado(self, estado): self.estado = estado

    def esta_activo(self): return self.estado == "ACTIVO"
    def suspender(self): self.estado = "SUSPENDIDO"

    def __str__(self):
        return f"Cliente[id_usuario={self.id_usuario}, estado={self.estado}]"