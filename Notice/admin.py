from django.contrib import admin

from .models import Notice
from .models import NoticeTemplate


@admin.register(NoticeTemplate)
class NoticeTemplateInformation(admin.ModelAdmin):
    list_display = (
        'title',
        'create_time',
    )


@admin.register(Notice)
class NoticeInformation(admin.ModelAdmin):
    list_display = (
        'title',
        'create_time',
        'customer',
        'is_read',
    )
