from django.urls import path

from . import views


app_name = 'main'

urlpatterns = [
    path('', views.get_main_page, name='main_page'),
    path('shops/', views.get_list_shops, name='shops'),
    path('storages/', views.get_list_storages, name='storages'),
    path('products/', views.get_list_products, name='products'),
    path('sold_products/', views.get_list_sold_products, name='sold_products'),
    path('storage/<int:id>/', views.product_list_by_storage,
         name='product_list_by_storage'),
    path('shop/<int:id>/', views.product_list_by_shop,
         name='product_list_by_shop'),
    path('about/', views.get_about_page, name='about'),
]
