from django.db import models


from users.models import User
from products.models import Product


class Basket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукты {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        my_sum = 0
        my_basket = Basket.objects.filter(user=self.user)
        for basket in my_basket:
            my_sum += basket.sum()
        return my_sum

    def total_quantity(self):
        my_quantity = 0
        my_basket = Basket.objects.filter(user=self.user)
        for basket in my_basket:
            my_quantity += basket.quantity
        return my_quantity
