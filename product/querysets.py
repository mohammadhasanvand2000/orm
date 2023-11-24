from django.db.models import QuerySet
from django.db.models import F, Q

class ProductQuerySet(QuerySet):
    def needs_restock(self):
        """Returns a queryset of products that their stock is less than 10."""
        return self.filter(stock__lt=10)

    def in_stock(self):
        """Returns a queryset of products that are in stock (stock is greater than or equal to 1)."""
        return self.filter(stock__gte=1)[:2]
