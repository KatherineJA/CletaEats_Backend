class Restaurante:

    def __init__(self):
        self.id = None
        self.nombre = ""
        self.cedula_juridica = ""
        self.direccion = ""
        self.tipo_comida = ""
        self.latitud = None
        self.longitud = None
        self.imagen = None
        self.id_encargado = None

    @classmethod
    def nuevo(cls, nombre, cedula_juridica, direccion, tipo_comida, latitud=None, longitud=None, id_encargado=None):
        r = cls()
        r.nombre = nombre
        r.cedula_juridica = cedula_juridica
        r.direccion = direccion
        r.tipo_comida = tipo_comida
        r.latitud = latitud
        r.longitud = longitud
        r.id_encargado = id_encargado
        return r

    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def get_nombre(self): return self.nombre
    def get_cedula_juridica(self): return self.cedula_juridica
    def get_tipo_comida(self): return self.tipo_comida

    def __str__(self):
        return f"Restaurante[id={self.id}, nombre={self.nombre}]"