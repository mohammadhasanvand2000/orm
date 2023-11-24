# tasks.py

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Sum
from utils.sms import SMS
from datetime import datetime
from order.models import *
from product.models import *
from user_management.models import *

@shared_task
def send_daily_sales_report():
  
    total_sales = Order.objects.filter(date__date=datetime.date.today()).aggregate(Sum('total_price'))['total_price__sum'] or 0

    
    products_to_restock = Product.objects.filter(stock__lt=10)

    
    managers = get_user_model().objects.filter(role=Manager)
    for manager in managers:
        message = f"Daily Sales Report:\nTotal Sales: ${total_sales}\nProducts to Restock: {', '.join(product.name for product in products_to_restock)}"
        sms = SMS(phone_number=manager.phone, message=message)
        sms.send()
