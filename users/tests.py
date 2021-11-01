from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from users.models import User


class TestMainSmokeTest(TestCase):
    status_code_success = 200
    status_code_render = 302
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekbrains'

    new_user_data = {
        'username': 'django2',
        'first_name': 'Django',
        'last_name': 'Django2',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'django2@mail.ru',
    }

    # 1 предустановленные параметры
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    # 2 выполнение теста
    def test_login(self):  # всегда начинаем с test_
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)  # работает ли сайт

        self.assertTrue(response.context['user'].is_anonymous)  # проверили, что юзер анонимный
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_render)

    def test_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_render)

        new_user = User.objects.get(username=self.new_user_data['username'])
        # формируем ссылку:
        activation_url = f'{settings.DOMAIN_NAME}/users/verify/{self.new_user_data["email"]}/{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    # 3 освобождение памяти от данных тестирования
    def tearDown(self) -> None:
        pass
