from django.urls import path
from AdminSecond.views.AdminIndex import AdminIndex
from AdminSecond.views.Profile import Profile
from AdminSecond.views.ChangePassword import ChangePassword
from AdminSecond.views.AdminThirdManagement import AdminThirdManagement
from AdminSecond.views.CustomerInformation import CustomerInformation
from AdminSecond.views.ActivityManagement import ActivityManagement
from AdminSecond.views.NoticeTemplateManagement import NoticeTemplateManagement
from AdminSecond.views.MerchandiseManagement import MerchandiseManagement
from AdminSecond.views.MerchandiseRequest import MerchandiseRequest
from AdminSecond.views.GiveIntegral import GiveIntegral

from utils.LogOut import admin_logout

app_name = 'AdminSecond'

urlpatterns = [
    # 二级管理员首页
    path('admin-index/', AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    # 三级管理员管理
    path('admin-third-management/', AdminThirdManagement.as_view(), name='admin_third_management'),
    # 客户信息
    path('customer-information/', CustomerInformation.as_view(), name='customer_information'),
    # 活动管理
    path('activity-management/', ActivityManagement.as_view(), name='activity_management'),
    # 客户通知管理
    path('notice-template-management/', NoticeTemplateManagement.as_view(), name='notice_template_management'),
    # 商品管理
    path('merchandise-management/', MerchandiseManagement.as_view(), name='merchandise_management'),
    # 商户请求
    path('merchandise-request/', MerchandiseRequest.as_view(), name='merchandise_request'),
    # 发放积分
    path('give-integral/', GiveIntegral.as_view(), name='give_integral'),

    # 登出
    path('logout/', admin_logout, name='logout'),
]