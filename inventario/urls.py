from django.urls import path
from .views import TiendaApiViews, TiendaApiViewsDetail



urlpatternsPerson = [
    
    path('v1/tienda/', TiendaApiViews.as_view()),
    
    path('v1/tienda/<int:id>', TiendaApiViewsDetail.as_view()),
    
    
    
    
    
    
    
]



