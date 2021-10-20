from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.core.cache import cache


import os
from products.models import ProductsCategory, Product


MODULE_DIR = os.path.dirname(__file__)

# Create your views here.


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        links_category = cache.get(key)

        if links_category is None:
            links_category = ProductsCategory.objects.filter(is_active=True)
            cache.set(key, links_category)
        return links_category
    else:
        return ProductsCategory.objects.filter(is_active=True)


def get_links_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        links_product = cache.get(key)

        if links_product is None:
            links_product = Product.objects.filter(is_active=True).select_related()
            cache.set(key, links_product)
        return links_product
    else:
        return Product.objects.filter(is_active=True).select_related()


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


class ProductsListView(ListView):
    model = Product
    template_name = 'products.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['category'] = get_links_category()
        # context['category'] = ProductsCategory.objects.all()
        # context['products'] = self.products_paginator(self)
        return context

    # def products_paginator(self, pk=None, page=1):
    #     products = Product.objects.filter(category_id=pk) if pk is not None else Product.objects.all()
    #     paginator = Paginator(products, per_page=3)
    #     try:
    #         products_paginator = paginator.page(page)
    #     except PageNotAnInteger:
    #         products_paginator = paginator.page(1)
    #     except EmptyPage:
    #         products_paginator = paginator.page(paginator.num_pages)
    #     return products_paginator

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
