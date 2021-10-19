from django.test import TestCase
from django.test.client import Client

from products.models import ProductsCategory, Product


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    #1 предустановленные параметры
    def setUp(self) -> None:
        category = ProductsCategory.objects.create(name='Test')
        Product.objects.create(category=category, name='product_test', price=100)

        self.client = Client()

    #2 выполнение теста
    def test_products_pages(self):  # всегда начинаем с test_
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_basket(self):  # всегда начинаем с test_
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 302)



    #3 освобождение памяти от данных тестирования
    def tearDown(self) -> None:
        pass
