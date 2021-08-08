from django.contrib import admin

from Merchandise.models import Merchandise
from Merchandise.models import GiveMerchandiseRecord


@admin.register(Merchandise)
class MerchandiseInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'remain_num',
        'is_delete',
    )


@admin.register(GiveMerchandiseRecord)
class GiveMerchandiseRecordInformation(admin.ModelAdmin):
    list_display = (
        'get_merchandise_name',
        'get_customer_name',
        'give_num',
        'give_time',
        'give_admin_name',
    )

    def get_merchandise_name(self, obj):
        return obj.merchandise.name

    def get_customer_name(self, obj):
        return obj.customer.name

