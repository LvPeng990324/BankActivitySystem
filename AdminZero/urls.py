from django.urls import path
from . import views

from utils.LogOut import admin_logout

app_name = 'AdminZero'

urlpatterns = [
    # 管理员首页
    path('admin-index/', views.AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', views.Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    # 一级管理员管理
    path('admin-first-management/', views.AdminFirstManagement.as_view(), name='admin_first_management'),
    # 二级管理员管理
    path('admin-second-mangement/', views.AdminSecondManagement.as_view(), name='admin_second_management'),
    # 三级管理员管理
    path('admin-third-management/', views.AdminThirdManagement.as_view(), name='admin_third_management'),
    # 客户信息
    path('customer-information/', views.CustomerInformation.as_view(), name='customer_information'),
    # 活动管理
    path('activity-management/', views.ActivityManagement.as_view(), name='activity_management'),
    # 通知模板管理
    path('notice-template-management/', views.NoticeTemplateManagement.as_view(), name='notice_template_management'),

    # 登出
    path('logout/', admin_logout, name='logout'),
]