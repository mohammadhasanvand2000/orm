from django.db import models

from product.querysets import ProductQuerySet


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=0)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name
