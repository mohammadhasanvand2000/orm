from django.test import TestCase

from product.models import Product


class TestProductQueryset(TestCase):
    fixtures = ['user_management/fixtures/user_management.json', 'product/fixtures/product.json', 'order/fixtures/order.json']

    def test_needs_restock(self):
        products_list = list(Product.objects.needs_restock().values_list('id', flat=True))
        self.assertEqual(products_list, [3])

    def test_in_stock(self):
        products_list = list(Product.objects.in_stock().values_list('id', flat=True))
        print(products_list)
        self.assertEqual(products_list, [1, 2])