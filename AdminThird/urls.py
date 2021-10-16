from django.urls import path
from AdminThird.views.AdminIndex import AdminIndex
from AdminThird.views.Profile import Profile
from AdminThird.views.ChangePassword import ChangePassword
from AdminThird.views.CustomerManagement import CustomerManagement
from AdminThird.views.NoticeView import NoticeView
from AdminThird.views.GenerateQRCode import GenerateQRCode
from AdminThird.views.GroupManagement import GroupManagement
from AdminThird.views.BatchSend import BatchSend
from AdminThird.views.MerchandiseManagement import MerchandiseManagement
from AdminThird.views.MerchandiseRequest import MerchandiseRequest

from utils.LogOut import admin_logout

app_name = 'AdminThird'

urlpatterns = [
    # 三级管理员首页
    path('admin-index/', AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    # 客户信息管理
    path('customer-management/', CustomerManagement.as_view(), name='customer_management'),
    # 通知查看
    path('notice-view/', NoticeView.as_view(), name='notice-view'),
    # 活动二维码
    path('generate-qrcode/', GenerateQRCode.as_view(), name='generate_qrcode'),
    # 组管理
    path('group-management/', GroupManagement.as_view(), name='group_management'),
    # 批量推送
    path('bacth-send/', BatchSend.as_view(), name='batch_send'),
    # 商品管理
    path('merchandise-management/', MerchandiseManagement.as_view(), name='merchandise_management'),
    # 商户请求
    path('merchandise-request/', MerchandiseRequest.as_view(), name='merchandise_request'),

    # 登出
    path('logout/', admin_logout, name='logout'),
]