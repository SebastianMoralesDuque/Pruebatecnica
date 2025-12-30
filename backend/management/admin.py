from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from shared_domain.models import Empresa, Producto

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nit', 'nombre', 'telefono')
    search_fields = ('nit', 'nombre')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'empresa')
    list_filter = ('empresa',)
    search_fields = ('codigo', 'nombre')
