from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Empresa, Producto, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'correo', 'username', 'is_administrator')

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_administrator'] = user.is_administrator
        token['email'] = user.correo
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_administrator'] = self.user.is_administrator
        data['email'] = self.user.correo
        return data
