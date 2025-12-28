from django.db import models

class EmpresaModel(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    class Meta:
        db_table = 'empresa'

    def __str__(self):
        return self.nombre

class ProductoModel(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    caracteristicas = models.TextField()
    precios = models.JSONField()
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.CASCADE, related_name='productos')

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre
