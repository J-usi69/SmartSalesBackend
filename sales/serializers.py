
from rest_framework import serializers
from .models import Sale, SaleDetail
from products.models import Product
from products.serializers import ProductSerializer
class SaleDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  #  No lo envíes desde el frontend
    class Meta:
        model = SaleDetail
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'subtotal']
class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'customer_name', 'customer_email', 'sale_date',
                  'payment_method', 'status', 'discount', 'total', 'details']
        read_only_fields = ['sale_date', 'total']
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        request = self.context.get('request')
        user = request.user if request else None
        total = 0
        for detail in details_data:
            subtotal = detail['quantity'] * detail['unit_price']
            detail['subtotal'] = subtotal  #  calcular subtotal
            total += subtotal
        discount = validated_data.get('discount', 0)
        total -= discount
        validated_data['total'] = total
        sale = Sale.objects.create(created_by=user, **validated_data)
        for detail in details_data:
            SaleDetail.objects.create(sale=sale, **detail)
        return sale
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                subtotal = detail['quantity'] * detail['unit_price']
                detail['subtotal'] = subtotal
                SaleDetail.objects.create(sale=instance, **detail)
        return instance
