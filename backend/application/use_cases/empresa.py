from shared_domain.models import Empresa
from shared_domain.exceptions import InvalidNITError

class GestionarEmpresaUseCase:
    @staticmethod
    def crear_empresa(data):
        try:
            empresa = Empresa(
                nit=data.get('nit'),
                nombre=data.get('nombre'),
                direccion=data.get('direccion'),
                telefono=data.get('telefono')
            )
            empresa.save()
            return empresa
        except InvalidNITError:
            raise
