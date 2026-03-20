class Restaurante:

    # Constructor default
    def __init__(self):
        self.id = None
        self.cedula_juridica = ""
        self.nombre = ""
        self.direccion = ""
        self.tipo_comida = ""
        self.combos = []

    # Constructor sobrecargado
    @classmethod
    def nuevo(cls, cedula_juridica, nombre, direccion, tipo_comida):
        r = cls()
        r.cedula_juridica = cedula_juridica
        r.nombre = nombre
        r.direccion = direccion
        r.tipo_comida = tipo_comida
        r.combos = []
        return r

    # Getters y setters
    def get_id(self): return self.id
    def set_id(self, id): self.id = id

    def get_nombre(self): return self.nombre
    def set_nombre(self, nombre): self.nombre = nombre

    def get_cedula_juridica(self): return self.cedula_juridica
    def set_cedula_juridica(self, cj): self.cedula_juridica = cj

    def get_tipo_comida(self): return self.tipo_comida
    def set_tipo_comida(self, tipo): self.tipo_comida = tipo

    # Métodos
    def agregar_combo(self, combo):
        self.combos.append(combo)

    def obtener_combo(self, numero):
        for combo in self.combos:
            if combo.numero == numero:
                return combo
        return None

    def __str__(self):
        return f"Restaurante[id={self.id}, nombre={self.nombre}, tipo={self.tipo_comida}]"