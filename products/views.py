from django.shortcuts import render

import os
import json
from products.models import ProductsCategory, Product


MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    context = {'title': "GeekShop"}
    return render(request, 'index.html', context)


def products(request):
    context = {"title": "Каталог"}
    context['products'] = Product.objects.all()
    context['category'] = ProductsCategory.objects.all()
    # path_file = os.path.join(MODULE_DIR, 'fixtures/goods.json')
    # context['products'] = json.load(open(path_file, encoding='utf-8'))
    return render(request, 'products.html', context)
