from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # APIs por app
    path('api/usuarios/', include('startapps.usuarios.urls')),
    path('api/catalogo/', include('startapps.catalogo.urls')),
    path('api/notas_ventas/', include('startapps.notas_ventas.urls')),
    path('api/reportes/', include('startapps.reportes.urls')),
    path('api/machin_learning/', include('startapps.machin_learning.urls')),

    path('api/v1/usuarios/', include('startapps.usuarios.urls')),
    path('api/v1/catalogo/', include('startapps.catalogo.urls')),
    path('api/v1/notas_ventas/', include('startapps.notas_ventas.urls')),
    path('api/v1/machin_learning/', include('startapps.machin_learning.urls')),
    path('api/v1/reportes/', include('startapps.reportes.urls')),
]


