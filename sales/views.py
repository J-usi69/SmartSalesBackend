from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Sale, SaleDetail
from .serializers import SaleSerializer
from django.utils.dateparse import parse_date
from django.db.models import Sum,F,Avg
from django.utils.timezone import make_aware
from datetime import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sales(request):
    sales = Sale.objects.all()
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SaleSerializer(sale)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sale(request):
    serializer = SaleSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SaleSerializer(sale, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Sale.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# enpoint para el reporte 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_selling_products(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except Exception:
        return Response({'error': 'Formato de fecha inválido. Usa YYYY-MM-DD.'}, status=400)

    top_products = (
        SaleDetail.objects
        .filter(sale__sale_date__range=[start, end])
        .values(
            'product_id',
            'product__name',
            'product__brand',
            'product__category__name'
        )
        .annotate(
            total_quantity_sold=Sum('quantity'),
            total_sales=Sum(F('quantity') * F('unit_price')),
            average_price=Avg('unit_price')
        )
        .order_by('-total_quantity_sold')
    )

    results = [
        {
            'product_id': p['product_id'],
            'name': p['product__name'],
            'brand': p['product__brand'],
            'category': p['product__category__name'],
            'average_unit_price': float(p['average_price']),
            'total_quantity_sold': p['total_quantity_sold'],
            'total_sales': float(p['total_sales'])
        }
        for p in top_products
    ]

    return Response(results)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productos_comprados_por_cliente(request):
    email = request.query_params.get('email')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not email or not start_date or not end_date:
        return Response({"error": "Parámetros 'email', 'start_date' y 'end_date' son requeridos."},
                        status=status.HTTP_400_BAD_REQUEST)

    detalles = SaleDetail.objects.filter(
        sale__customer_email=email,
        sale__sale_date__range=[start_date, end_date]
    ).values(
        'product__id',
        'product__name',
        'product__brand',
        'product__category__name'
    ).annotate(
        cantidad_total=Sum('quantity'),
        precio_unitario=F('unit_price'),
        subtotal=Sum(F('quantity') * F('unit_price'))
    ).order_by('-cantidad_total')

    return Response(detalles)   
