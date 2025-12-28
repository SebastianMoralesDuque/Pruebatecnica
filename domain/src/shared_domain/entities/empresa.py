from ..exceptions import InvalidNITError

class Empresa:
    def __init__(self, nit: str, nombre: str, direccion: str, telefono: str):
        if not nit:
            raise InvalidNITError("El NIT es obligatorio")
        self.nit = nit
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def __str__(self):
        return self.nombre
