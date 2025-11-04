from django.urls import path
from . import views
urlpatterns = [
    path('sales/', views.list_sales),
    path('sales/<int:pk>/', views.get_sale),
    path('sales/create/', views.create_sale),
    path('sales/update/<int:pk>/', views.update_sale),
    path('sales/delete/<int:pk>/', views.delete_sale),
      #para reporte 
    path('report/top-selling-products/', views.top_selling_products),
    path('report/products-by-customer/', views.productos_comprados_por_cliente),

]

