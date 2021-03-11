from django.urls import path
from . import views

from utils.LogOut import admin_logout

app_name = 'AdminThird'

urlpatterns = [
    # 三级管理员首页
    path('admin-index/', views.AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', views.Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    # 客户信息管理
    path('customer-management/', views.CustomerManagement.as_view(), name='customer_management'),
    # 通知查看
    path('notice-view/', views.NoticeView.as_view(), name='notice-view'),
    # 活动二维码
    path('generate-qrcode/', views.GenerateQRCode.as_view(), name='generate_qrcode'),
    # 组管理
    path('group-management/', views.GroupManagement.as_view(), name='group_management'),
    # 批量推送
    path('bacth-send/', views.BatchSend.as_view(), name='batch_send'),

    # 登出
    path('logout/', admin_logout, name='logout'),
]