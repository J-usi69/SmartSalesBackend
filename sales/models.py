from django.db import models
from django.conf import settings
from products.models import Product
class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField(blank=True, null=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    PAYMENT_METHOD_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    STATUS_CHOICES = [
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sales'
    )
    def __str__(self):
        return f"Sale #{self.id} - {self.customer_name}"
class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
