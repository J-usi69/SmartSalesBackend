from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateUpdateSerializer, CategorySerializer
from django.db.models import F
# from accounts.utils import enviar_notificacion_fcm
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from server.firebase.Utils import enviar_notificacion_fcm  # Asegúrate que el import funcione con tu estructura

# ---------- CATEGORÍAS ----------

@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# ---------- PRODUCTOS ----------

@api_view(['GET'])
def list_products(request):
    products = Product.objects.select_related('category').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    serializer = ProductCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(ProductSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(ProductSerializer(serializer.instance).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# carga masiva 
@api_view(['POST'])
def bulk_create_products(request):
    serializer = ProductSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Productos creados correctamente", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_productos_bajo_stock(request):
    productos_bajo_stock = Product.objects.filter(stock__lt=F('stock_minimo'))

    if productos_bajo_stock.exists():
        responsables = CustomUser.objects.filter(role__name="Admin")  # 🔁 o según tu lógica
        for producto in productos_bajo_stock:
            for responsable in responsables:
                if responsable.fcm_token:
                    enviar_notificacion_fcm(
                        responsable.fcm_token,
                        f" Stock bajo: {producto.name}",
                        f"Solo quedan {producto.stock} unidades. Mínimo recomendado: {producto.stock_minimo}"
                    )

    return Response({"message": "Notificaciones enviadas si había stock bajo."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alerta_stock_sms(request):
    productos = Product.objects.filter(stock__lte=F('stock_minimo'))
    serializer = ProductSerializer(productos, many=True)
    return Response(serializer.data)