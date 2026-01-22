from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from rest_framework.views import APIView
from .serializers import UserSerializersProd


#vistas para consultar todos los productos
class TiendaApiViews(APIView):
    def get(self,request):
        serial= UserSerializersProd(Producto.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serial.data)
        
    
    def post(self,request):
        serial=UserSerializersProd(data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(status=status.HTTP_201_CREATED, data=serial.data)

class TiendaApiViewsDetail(APIView):
    
    def get_object(self,pk):
        all= Producto
        try:
            return all.objects.get( pk=pk)
        except all.DoesNotExist:
            return None
    
    def get(self,request,id):
        post= self.get_object(id)
        serial=UserSerializersProd(post)
        return Response(status=status.HTTP_200_OK, data=serial.data)
    
    def put(self,request,id):
        post=self.get_object(id)
        if(post==None):
            return Response(status=status.HTTP_200_OK, data={'error':'Not found data'})
        serial=UserSerializersProd(post, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(status=status.HTTP_200_OK, data=serial.data)
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        producto=self.get_object(id)
        producto.delete()
        response={'delete': True}
        return Response(status=status.HTTP_200_OK, data=response)            
    
