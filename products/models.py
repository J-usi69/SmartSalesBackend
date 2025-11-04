
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.CharField(max_length=50)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    image = models.URLField()  # o models.ImageField si querés usar archivos locales

    def __str__(self):
        return self.name

    def total_vendido(self):
        return self.saledetail_set.aggregate(total=sum('quantity'))['total'] or 0