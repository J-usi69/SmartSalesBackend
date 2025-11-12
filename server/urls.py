"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # si todavía usás vistas en server/views.py
from accounts.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.http import JsonResponse

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vista simple para mostrar algo en la raíz
def health_check(request):
    return JsonResponse({"message": "Backend Django funcionando en Render "})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Rutas de tu app 'accounts'
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('sales.urls')),

    # https://ecommercebackend-7m3u.onrender.com

]



