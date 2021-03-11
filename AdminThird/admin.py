from django.contrib import admin

from .models import AdminThird


@admin.register(AdminThird)
class AdminThirdInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'job_num',
    )
