from shared_domain.models import Empresa, Producto
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    correo = models.EmailField(unique=True)
    is_administrator = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.correo

