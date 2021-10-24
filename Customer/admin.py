from django.contrib import admin

from .models import Customer
from .models import IntegralGiveLog


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


@admin.register(IntegralGiveLog)
class IntegralGiveLogInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'get_customer_name',
        'admin_name',
        'give_num',
        'create_time',
    )

    def get_customer_name(self, obj):
        return obj.customer.name

