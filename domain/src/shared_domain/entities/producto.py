from django.db import models
from ..exceptions import BusinessRuleError, InvalidPriceError
from .empresa import Empresa

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    caracteristicas = models.TextField()
    precios = models.JSONField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def clean(self):
        if not self.precios:
            raise InvalidPriceError("El producto debe tener al menos un precio")
        
        # Validate prices are non-negative
        for currency, value in self.precios.items():
            try:
                if float(value) < 0:
                    raise InvalidPriceError(f"El precio en {currency} no puede ser negativo.")
            except (ValueError, TypeError):
                raise InvalidPriceError(f"El precio en {currency} debe ser un número válido.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def precio_en(self, moneda):
        # Allow default dict usage if self.precios is fetched as dict (JSONField)
        if hasattr(self.precios, 'get'):
             if moneda not in self.precios:
                 raise BusinessRuleError(f"Moneda {moneda} no disponible")
             return self.precios[moneda]
        return None # Should not happen if validated

    def __str__(self):
        return self.nombre
