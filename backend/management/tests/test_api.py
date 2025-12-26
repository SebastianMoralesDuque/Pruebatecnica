import pytest
from rest_framework.test import APIClient
from management.models import User, Empresa, Producto
from unittest.mock import patch

@pytest.fixture
def auth_client():
    client = APIClient()
    user = User.objects.create_superuser(correo='admin_test@example.com', username='admin_test', password='password', is_administrator=True)
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def regular_client():
    client = APIClient()
    user = User.objects.create_user(correo='user_test@example.com', username='user_test', password='password', is_administrator=False)
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_list_empresas(auth_client):
    Empresa.objects.create(nit="123", nombre="Test Co")
    response = auth_client.get('/api/empresas/')
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_create_producto(auth_client):
    empresa = Empresa.objects.create(nit="123", nombre="Test Co")
    data = {
        "codigo": "P1",
        "nombre": "Producto Test",
        "caracteristicas": "Algo",
        "precios": {"USD": 10},
        "empresa": "123"
    }
    response = auth_client.post('/api/productos/', data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_regular_user_cannot_create_empresa(regular_client):
    data = {"nit": "999", "nombre": "No Permission"}
    response = regular_client.post('/api/empresas/', data)
    assert response.status_code == 403

@pytest.mark.django_db
@patch('management.views.ProductoViewSet.generate_ai_content')
def test_generate_inventory_pdf(mock_ai, auth_client):
    mock_ai.return_value = "Análisis de prueba"
    response = auth_client.get('/api/productos/generate_inventory_pdf/')
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'

@pytest.mark.django_db
@patch('management.views.Transaction')
@patch('management.views.Message')
@patch('management.views.Keypair')
@patch('management.views.Client')
@patch('management.views.ProductoViewSet.generate_ai_content')
def test_certify_inventory(mock_ai, mock_solana, mock_kp, mock_msg, mock_tx, auth_client):
    mock_ai.return_value = "Análisis IA"
    
    # Mock Solana transaction flow
    mock_client_inst = mock_solana.return_value
    mock_client_inst.get_latest_blockhash.return_value.value.blockhash = "fake_blockhash"
    mock_client_inst.send_transaction.return_value.value = "fake_tx_hash"
    
    # Mock Keypair to avoid real key validation
    mock_kp.from_seed.return_value.pubkey.return_value = "fake_pubkey"
    
    response = auth_client.post('/api/productos/certify_inventory/')
    if response.status_code != 200:
        print(f"\nResponse data: {response.data}")
    assert response.status_code == 200
    assert 'txHash' in response.data
