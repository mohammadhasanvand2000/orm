from django.db import models
from django.db.models import QuerySet, Sum, F

class OrderQuerySet(QuerySet):
    def by_customer(self, customer):
        return self.filter(customer=customer)

    def total_price(self):
        return float(self.aggregate(Sum('total_price'))['total_price__sum'] or 0.00)

    def total_price_by_customer(self, customer):
        return float(self.filter(customer=customer).aggregate(Sum('total_price'))['total_price__sum'] or 0.00)

    def submitted_in_date(self, date_value):
        return self.filter(date__date=date_value)
