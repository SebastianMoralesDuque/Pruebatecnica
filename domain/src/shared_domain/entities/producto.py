from ..exceptions import BusinessRuleError, InvalidPriceError

class Producto:
    def __init__(self, codigo: str, nombre: str, caracteristicas: str, precios: dict, empresa=None):
        if not precios:
            raise InvalidPriceError("El producto debe tener al menos un precio")
        
        # Validate prices are non-negative
        for currency, value in precios.items():
            try:
                if float(value) < 0:
                    raise InvalidPriceError(f"El precio en {currency} no puede ser negativo.")
            except (ValueError, TypeError):
                raise InvalidPriceError(f"El precio en {currency} debe ser un número válido.")

        self.codigo = codigo
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.precios = precios
        self.empresa = empresa

    def precio_en(self, moneda):
        if moneda not in self.precios:
            raise BusinessRuleError(f"Moneda {moneda} no disponible")
        return self.precios[moneda]

    def __str__(self):
        return self.nombre
