from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView

import os
from products.models import ProductsCategory, Product


MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def index(request):
    context = {'title': "GeekShop"}
    return render(request, 'index.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Подробно о товаре'
        return context


# def product(request, id):
#     product = Product.objects.filter(id=id)
#     context = {
#         'title': 'Подробно о товаре',
#         'product': product
#     }
#     return render(request, 'product.html', context)


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['category'] = ProductsCategory.objects.all()
        context['products'] = self.products_paginator(self)
        return context

    def products_paginator(self, pk=None, page=1):
        products = Product.objects.filter(category_id=pk) if pk is not None else Product.objects.all()
        paginator = Paginator(products, per_page=3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        return products_paginator

# def products(request, id=None, page=1):
#     products = Product.objects.filter(category_id=id) if id is not None else Product.objects.all()
#     paginator = Paginator(products, per_page=3)
#     try:
#         products_paginator = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context = {"title": "Каталог"}
#     context['category'] = ProductsCategory.objects.all()
#     context['products'] = products_paginator
#     return render(request, 'products.html', context)
