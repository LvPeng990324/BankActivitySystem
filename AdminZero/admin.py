from django.contrib import admin

from AdminZero.models import AdminZero


@admin.register(AdminZero)
class AdminZeroInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'job_num',
    )


