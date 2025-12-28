from infrastructure.django_models.models import ProductoModel, EmpresaModel
from shared_domain.entities.producto import Producto
from shared_domain.exceptions import BusinessRuleError

class GestionarProductoUseCase:
    @staticmethod
    def crear_producto(data):
        # 1. Validar con Entidad de Dominio Puro
        try:
            # Note: We don't necessarily need the full Empresa entity here if we just want to validate Producto
            empresa_id = data.get('empresa')
            if not empresa_id:
                raise BusinessRuleError("La empresa es obligatoria")
            
            # This will trigger our pure Python validations (precios, etc.)
            domain_producto = Producto(
                codigo=data.get('codigo'),
                nombre=data.get('nombre'),
                caracteristicas=data.get('caracteristicas'),
                precios=data.get('precios')
            )
        except BusinessRuleError:
            raise

        # 2. Persistir en Infraestructura
        try:
            empresa_model = EmpresaModel.objects.get(nit=empresa_id)
        except EmpresaModel.DoesNotExist:
            raise BusinessRuleError(f"Empresa con NIT {empresa_id} no encontrada.")

        producto_model = ProductoModel.objects.create(
            codigo=domain_producto.codigo,
            nombre=domain_producto.nombre,
            caracteristicas=domain_producto.caracteristicas,
            precios=domain_producto.precios,
            empresa=empresa_model
        )
        return producto_model
