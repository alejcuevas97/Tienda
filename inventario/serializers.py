from rest_framework.serializers import ModelSerializer
from .models import Producto

#creando las serializacion de registro
class UserSerializersProd(ModelSerializer):
    class Meta:
        model= Producto
        fields=['id','nombre','descripcion','precio']
        
