from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'gender',
        'town',
        'village',
        'group',
        'street',
        'phone',
        'tag',
        'is_vip',
    )

