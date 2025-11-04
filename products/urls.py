from django.urls import path
from . import views

urlpatterns = [
    # Categorías
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/update/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    # Productos
    path('products/', views.list_products, name='list_products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/bulk-create/', views.bulk_create_products, name='bulk-create-products'),
    path('products/alerta-stock/',  views.verificar_productos_bajo_stock),
    path('products/alerta-stock-sms/',  views.alerta_stock_sms),


]
