# Предположим, что в нашем магазине объявлено несколько акций:
# при оплате заказа в течение 12 часов - скидка 30%;
# при оплате заказа в течение суток - скидка 15%,
# на остальные товары - скидка 5%.
# Выведем данные о величине скидки на каждый элемент заказа с учетом акции следующим образом. Сначала выводим позиции,
# которые попали под первую акцию в порядке увеличения выгоды. Затем позиции, которые попали под вторую акцию в порядке
# уменьшения выгоды. Потом - остальные позиции, снова в порядке увеличения выгоды. Чередование можно реализовать и для
# большего количества предложений. Таким образом получим своего рода волны, по которым можно найти самые выгодные
# товары на границах акций.
# Чтобы сэкономить время и не создавать новых атрибутов модели, будем считать датой оплаты заказа значение его
# атрибута «updated».  На самом деле в будущем для хранения даты оплаты можем создать, например, атрибут «paid».

from datetime import timedelta
from django.core.management.base import BaseCommand

from ordersapp.models import OrderItem
from django.db.models import Q, F, When, Case, IntegerField, DecimalField
from prettytable import PrettyTable


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated__lte=F('order__created')+action_1_time_delta)  # lte - меньше или равно
        action_2_condition = Q(order__updated__gt=F('order__created')+action_1_time_delta)\
                             & Q(order__updated__lte=F('order__created')+action_2_time_delta)  # gt - больше
        action_3_condition = Q(order__updated__gt=F('order__created') + action_2_time_delta)

        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        ).order_by('action_order', 'total_price').select_related()

        t_list = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Время'])
        t_list.align = 'l'
        for orderitem in test_orders:
            t_list.add_row([f'{orderitem.action_order} заказ № {orderitem.pk}',
                            f'{orderitem.product.name:15}',
                            f'{abs(orderitem.total_price):6.2f} руб.',
                            orderitem.order.updated - orderitem.order.created])

        print(t_list)
