from django.contrib import admin

from .models import AdminSecond


@admin.register(AdminSecond)
class AdminSecondInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'job_num',
    )
