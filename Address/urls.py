from django.urls import path
from . import views
from . import apis

app_name = 'Address'

urlpatterns = [
    # 村子
    path('village-information/', apis.village_information, name='village_information'),
    # 组
    path('group-information/', apis.group_information, name='group_information'),

]
