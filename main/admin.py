from django.contrib import admin
from .models import StorageUnit, Customer, Order


my_models = [StorageUnit, Customer, Order]
""" admin.site.register(my_models) """


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("pk", "fullname", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "customer", "start_date")


@admin.register(StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
