from shared_domain.models import Empresa, Producto
from shared_domain.exceptions import BusinessRuleError, EntityNotFoundError

class GestionarProductoUseCase:
    @staticmethod
    def crear_producto(data):
        try:
            empresa_id = data.get('empresa')
            if not empresa_id:
                raise BusinessRuleError("La empresa es obligatoria")
            
            try:
                empresa = Empresa.objects.get(nit=empresa_id)
            except Empresa.DoesNotExist:
                raise EntityNotFoundError(f"Empresa con NIT {empresa_id} no encontrada.")

            producto = Producto(
                codigo=data.get('codigo'),
                nombre=data.get('nombre'),
                caracteristicas=data.get('caracteristicas'),
                precios=data.get('precios'),
                empresa=empresa
            )
            producto.save()
            return producto
        except BusinessRuleError:
            raise
