from django.contrib import admin

from .models import Activity
from .models import ActivityRecord


@admin.register(Activity)
class ActivityInformation(admin.ModelAdmin):
    list_display = (
        'name',
        'create_time',
        'end_time',
        'is_delete'
    )


@admin.register(ActivityRecord)
class ActivityRecordInformation(admin.ModelAdmin):
    list_display = (
        'activity',
        'customer',
        'admin_third',
        'create_time',
    )
