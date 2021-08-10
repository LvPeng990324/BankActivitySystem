from django.urls import path
from AdminZero.views.AdminIndex import AdminIndex
from AdminZero.views.Profile import Profile
from AdminZero.views.ChangePassword import ChangePassword
from AdminZero.views.AdminFirstManagement import AdminFirstManagement
from AdminZero.views.AdminSecondManagement import AdminSecondManagement
from AdminZero.views.AdminThirdManagement import AdminThirdManagement
from AdminZero.views.CustomerInformation import CustomerInformation
from AdminZero.views.ActivityManagement import ActivityManagement
from AdminZero.views.NoticeTemplateManagement import NoticeTemplateManagement
from AdminZero.views.MerchandiseManagement import MerchandiseManagement

from utils.LogOut import admin_logout

app_name = 'AdminZero'

urlpatterns = [
    # 管理员首页
    path('admin-index/', AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    # 一级管理员管理
    path('admin-first-management/', AdminFirstManagement.as_view(), name='admin_first_management'),
    # 二级管理员管理
    path('admin-second-mangement/', AdminSecondManagement.as_view(), name='admin_second_management'),
    # 三级管理员管理
    path('admin-third-management/', AdminThirdManagement.as_view(), name='admin_third_management'),
    # 客户信息
    path('customer-information/', CustomerInformation.as_view(), name='customer_information'),
    # 活动管理
    path('activity-management/', ActivityManagement.as_view(), name='activity_management'),
    # 通知模板管理
    path('notice-template-management/', NoticeTemplateManagement.as_view(), name='notice_template_management'),
    # 商品管理
    path('merchandise-management/', MerchandiseManagement.as_view(), name='merchandise_management'),

    # 登出
    path('logout/', admin_logout, name='logout'),
]