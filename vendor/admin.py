from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_approved','created_at')
    list_display_links = ('user','vendor_name')
    list_filter = ('is_approved',)
    search_fields = ('vendor_name',)
    list_editable = ('is_approved',)
    list_per_page = 10

admin.site.register(Vendor,VendorAdmin)