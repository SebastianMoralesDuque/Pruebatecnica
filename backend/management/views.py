from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

# Entities & Exceptions
from shared_domain.exceptions import BusinessRuleError

# Models
from .models import Empresa, Producto

# Serializers
from .serializers import EmpresaSerializer, ProductoSerializer, MyTokenObtainPairSerializer

# Application Layer (Use Cases)
from application.use_cases.inventario import ProcesarInventarioUseCase, CertificarInventarioUseCase
from application.use_cases.producto import GestionarProductoUseCase

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_administrator

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'nit'

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]

    def create(self, request, *args, **kwargs):
        # Delegar totalmente al Caso de Uso
        producto_model = GestionarProductoUseCase.crear_producto(request.data)
        serializer = self.get_serializer(producto_model)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def generate_inventory_pdf(self, request):
        tx_hash = request.query_params.get('tx_hash')
        
        # Orquestar vía Caso de Uso
        resultado = ProcesarInventarioUseCase.ejecutar(tx_hash=tx_hash)
        
        return HttpResponse(resultado["pdf_content"], content_type='application/pdf')

    @action(detail=False, methods=['post'])
    def send_inventory_pdf(self, request):
        email = request.data.get('email')
        tx_hash = request.data.get('tx_hash')
        
        if not email:
            raise BusinessRuleError("El email es requerido.")

        # Orquestar vía Caso de Uso
        ProcesarInventarioUseCase.ejecutar(email=email, tx_hash=tx_hash, send_email=True)
        
        return Response({"message": f"Reporte enviado exitosamente a {email}"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def certify_inventory(self, request):
        # Orquestar vía Caso de Uso
        resultado = CertificarInventarioUseCase.ejecutar()
        
        return Response(resultado, status=status.HTTP_200_OK)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
