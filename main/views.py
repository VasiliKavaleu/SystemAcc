from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Shop, Storage, ProductOnStorage, SoldProduct
from .services import get_latest_news
from .paginator_helper import pg_records


def get_main_page(request):
    return render(request, 'main.html',
                  {
                    'data_set1': get_latest_news()[0],
                    'data_set2': get_latest_news()[1],
                  })


@login_required
def get_list_shops(request):
    """Displaying list of shops."""
    shops = Shop.objects.all()
    context = pg_records(request, shops, 3)
    return render(request, 'list_shops.html',
                  {'shops': context})


@login_required
def get_list_storages(request):
    """Displaying list of storages."""
    storages = Storage.objects.all()
    context = pg_records(request, storages, 3)
    return render(request, 'list_storages.html',
                  {'storages': context})


@login_required
def get_list_products(request):
    """Displaying list of available products."""
    available_products = ProductOnStorage.objects.all()
    context = pg_records(request, available_products, 3)
    return render(request, 'list_available_products.html',
                  {'available_products': context})


@login_required
def get_list_sold_products(request):
    """Displaying list of sold products."""
    sold_products = SoldProduct.objects.all()
    context = pg_records(request, sold_products, 3)
    return render(request, 'list_sold_products.html',
                  {'sold_products': context})


@login_required
def product_list_by_storage(request, id):
    """Displaying list of products by storage."""
    products = ProductOnStorage.objects.filter(storage__id=id)
    storage = get_object_or_404(Storage, id=id)
    context = pg_records(request, products, 3)
    return render(request, 'products_of_storage.html',
                  {'products_of_storage': context, 'storage': storage})


@login_required
def product_list_by_shop(request, id):
    """Displaying list of products by shop."""
    products = ProductOnStorage.objects.filter(shops__id=id)
    shop = get_object_or_404(Shop, id=id)
    context = pg_records(request, products, 3)
    return render(request, 'products_of_shop.html',
                  {'products_of_shop': context, 'shop': shop})


def get_about_page(request):
    return render(request, 'about.html')
