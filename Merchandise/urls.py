from django.urls import path

from Merchandise.apis.get_merchandise_info import get_merchandise_info

app_name = 'Merchandise'

urlpatterns = [
    # 获取商品信息接口
    path('get-merchandise-info/', get_merchandise_info, name='get_merchandise_info'),
]
