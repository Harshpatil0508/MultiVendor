from django.contrib import admin
from .models import *
# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','vendor', 'created_at', 'updated_at')
    # list_editable = ('vendor',)
    search_fields = ('category_name','vendor__vendor_name')
    list_filter = ('vendor',)

class productAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name','vendor', 'category', 'price', 'is_available', 'created_at', 'updated_at')
    # list_editable = ('vendor',)
    search_fields = ('product_name','category__category_name','vendor__vendor_name','price')
    list_filter = ('is_available',)

admin.site.register(Category, categoryAdmin)
admin.site.register(Product, productAdmin)