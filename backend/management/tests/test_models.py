import pytest
from management.models import Empresa, Producto

@pytest.mark.django_db
def test_empresa_creation():
    empresa = Empresa.objects.create(
        nit="123456789",
        nombre="Empresa Test",
        direccion="Calle Falsa 123",
        telefono="555-1234"
    )
    assert empresa.nit == "123456789"
    assert str(empresa) == "Empresa Test"

@pytest.mark.django_db
def test_producto_creation():
    empresa = Empresa.objects.create(nit="111", nombre="Empresa Prod")
    producto = Producto.objects.create(
        codigo="PROD001",
        nombre="Laptop",
        caracteristicas="16GB RAM, 512GB SSD",
        precios={"USD": 1000, "COP": 4000000},
        empresa=empresa
    )
    assert producto.codigo == "PROD001"
    assert producto.empresa.nombre == "Empresa Prod"
    assert str(producto) == "Laptop"
