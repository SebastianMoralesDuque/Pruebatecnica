import pytest
from rest_framework.test import APIClient
from management.models import User, Empresa, Producto
from unittest.mock import patch

@pytest.fixture
def auth_client():
    client = APIClient()
    user = User.objects.create_superuser(
        correo='admin@test.com',
        username='admin',
        password='password123',
        is_administrator=True
    )
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_list_empresas(auth_client):
    Empresa.objects.create(nit='123', nombre='Test Inc', direccion='Calle 1', telefono='555')
    response = auth_client.get('/api/empresas/')
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_create_producto(auth_client):
    empresa = Empresa.objects.create(nit='456', nombre='Comp A', direccion='D1', telefono='T1')
    data = {
        "codigo": "P001",
        "nombre": "Producto Test",
        "caracteristicas": "Algo",
        "precios": {"USD": 10, "COP": 40000},
        "empresa": empresa.nit
    }
    response = auth_client.post('/api/productos/', data, format='json')
    assert response.status_code == 201
    assert response.data['nombre'] == "Producto Test"

@pytest.mark.django_db
def test_create_producto_precio_negativo(auth_client):
    empresa = Empresa.objects.create(nit='789', nombre='Comp B', direccion='D2', telefono='T2')
    data = {
        "codigo": "P002",
        "nombre": "Producto Malo",
        "caracteristicas": "Algo",
        "precios": {"USD": -1},
        "empresa": empresa.nit
    }
    response = auth_client.post('/api/productos/', data, format='json')
    assert response.status_code == 400
    assert response.data['code'] == "InvalidPriceError"
    assert "no puede ser negativo" in response.data['error']

@pytest.mark.django_db
@patch('infrastructure.services.ai_service.AIService.generate_inventory_analysis')
def test_generate_inventory_pdf(mock_ai, auth_client):
    mock_ai.return_value = "Análisis IA"
    response = auth_client.get('/api/productos/generate_inventory_pdf/')
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'

@pytest.mark.django_db
@patch('infrastructure.services.blockchain_service.BlockchainService.certify_data')
@patch('infrastructure.services.ai_service.AIService.generate_inventory_analysis')
def test_certify_inventory(mock_ai, mock_blockchain, auth_client):
    mock_ai.return_value = "Análisis IA"
    mock_blockchain.return_value = {
        "txHash": "fake_tx_hash",
        "pdf_hash": "fake_pdf_hash",
        "status": "SUCCESS"
    }
    
    response = auth_client.post('/api/productos/certify_inventory/')
    assert response.status_code == 200
    assert 'txHash' in response.data
