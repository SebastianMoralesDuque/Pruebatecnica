from infrastructure.django_models.models import EmpresaModel, ProductoModel
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    correo = models.EmailField(unique=True)
    is_administrator = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.correo

# Alias for backward compatibility if needed, though we should use Infrastructure names
Empresa = EmpresaModel
Producto = ProductoModel
