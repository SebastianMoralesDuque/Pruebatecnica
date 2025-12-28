import pytest
from management.models import Empresa, Producto

@pytest.mark.django_db
def test_empresa_creation():
    empresa = Empresa.objects.create(
        nit="123456789-0",
        nombre="Empresa Test",
        direccion="Calle Falsa 123",
        telefono="3001234567"
    )
    assert empresa.nombre == "Empresa Test"
    assert str(empresa) == "Empresa Test"

@pytest.mark.django_db
def test_producto_creation():
    empresa = Empresa.objects.create(
        nit="987654321-0",
        nombre="Empresa Prod",
        direccion="Avenida Siempre Viva 742",
        telefono="3119876543"
    )
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
