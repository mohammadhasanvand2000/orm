from django.db import models
from order.enums import OrderStatus
from order.querysets import OrderQuerySet
from decimal import Decimal

class Order(models.Model):
    customer = models.ForeignKey('user_management.Customer', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=OrderStatus.PENDING, choices=OrderStatus.choices)
    total_price = models.FloatField(default=0)
    
    objects = OrderQuerySet.as_manager()

    def calculate_total_price(self):
        latest_orderitem = self.orderitem_set.values(
            'product__price',
        ).order_by('id').first()

        latest_orderitem_price = Decimal(latest_orderitem['product__price'])
        
      

    
        new_total_price = Decimal(str(self.total_price)) + Decimal(str(latest_orderitem_price))
        new_total_price = round(new_total_price, 2)
    

        self.total_price = new_total_price
    

        self.save()


        print(f"After update - total_price: {self.total_price}")

        return self.total_price
    
    def accept(self):
        self.status = OrderStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = OrderStatus.REJECTED
        self.save()

    def deliver(self):
        self.status = OrderStatus.DELIVERED
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()
    
class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order.customer.user.username} - {self.product.name}'
    
    def update_order_total_price(sender, instance, **kwargs):
        instance.order.calculate_total_price()
        instance.order.save()

    def save(self, *args, **kwargs):
        """You can not modify this method"""
        self.order.total_price = self.order.calculate_total_price()
        self.order.save()
        super().save(*args, **kwargs)