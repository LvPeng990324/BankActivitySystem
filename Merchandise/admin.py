from django.contrib import admin

from Merchandise.models import Merchandise


@admin.register(Merchandise)
class MerchandiseInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'remain_num',
        'is_delete',
    )

