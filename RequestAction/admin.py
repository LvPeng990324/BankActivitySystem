from django.contrib import admin

from RequestAction.models import RequestAction


@admin.register(RequestAction)
class RequestActionInformation(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'get_customer_name',
        'start_date',
        'end_date',
        'is_finished',
    )

    def get_customer_name(self, obj):
        return obj.customer.name



