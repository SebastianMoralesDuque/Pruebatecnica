import pytest
from shared_domain.entities import Empresa, Producto
from shared_domain.exceptions import BusinessRuleError, InvalidNITError, InvalidPriceError

def test_empresa_validation():
    with pytest.raises(InvalidNITError, match="El NIT es obligatorio"):
        Empresa(nit="", nombre="Test", direccion="...", telefono="...")

def test_producto_precio_moneda():
    producto = Producto(
        codigo="A1",
        nombre="Laptop",
        caracteristicas="16GB",
        precios={"USD": 1000, "COP": 4000000}
    )
    assert producto.precio_en("USD") == 1000
    assert producto.precio_en("COP") == 4000000
    
    with pytest.raises(BusinessRuleError, match="Moneda EUR no disponible"):
        # Note: precio_en still raises BusinessRuleError which is a base for pricing errors or generic business errors
        producto.precio_en("EUR")

def test_producto_precios_obligatorios():
    with pytest.raises(InvalidPriceError, match="El producto debe tener al menos un precio"):
        Producto(codigo="B1", nombre="X", caracteristicas="Y", precios={})

def test_producto_precios_negativos():
    with pytest.raises(InvalidPriceError, match="El precio en USD no puede ser negativo"):
        Producto(codigo="B1", nombre="X", caracteristicas="Y", precios={"USD": -10})
