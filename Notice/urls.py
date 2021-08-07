from django.urls import path

from Notice.apis.get_notice_template import get_notice_template

app_name = 'Notice'

urlpatterns = [
    path('get-notice-template/', get_notice_template, name='get_notice_template'),
]
