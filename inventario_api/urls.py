from django.contrib import admin
from django.urls import path, include, re_path
from inventario.urls import urlpatternsPerson 
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include(urlpatternsPerson)),
    
    re_path ('register/', views.register),
    
    re_path('login/', views.login),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
]
