from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
from products.models import ProductsCategory, Product


MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    context = {'title': "GeekShop"}
    return render(request, 'index.html', context)


def products(request, id=None, page=1):
    products = Product.objects.filter(category_id=id) if id != None else Product.objects.all()
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {"title": "Каталог"}
    context['category'] = ProductsCategory.objects.all()
    context['products'] = products_paginator
    return render(request, 'products.html', context)
