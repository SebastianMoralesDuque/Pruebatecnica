from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    correo = models.EmailField(unique=True)
    is_administrator = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.correo

class Empresa(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    caracteristicas = models.TextField()
    precios = models.JSONField()  # E.g., {"USD": 100, "COP": 400000}
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre
