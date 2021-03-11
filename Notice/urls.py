from django.urls import path

from . import views
from . import apis

app_name = 'Notice'

urlpatterns = [
    path('get-notice-template/', apis.get_notice_template, name='get_notice_template'),
]
