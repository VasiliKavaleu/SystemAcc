from django.contrib import admin

from .models import Storage, Shop, Category, \
                    Product, SoldProduct, ProductOnStorage


admin.site.register(Storage)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SoldProduct)


@admin.register(ProductOnStorage)
class ProductOnStorageAdmin(admin.ModelAdmin):
    list_display = ['product']
