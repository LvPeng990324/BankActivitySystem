from django.contrib import admin

from .models import AdminFirst


@admin.register(AdminFirst)
class AdminFirstInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'job_num',
    )
