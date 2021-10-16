from django.urls import path
from AdminFirst.views.AdminIndex import AdminIndex
from AdminFirst.views.Profile import Profile
from AdminFirst.views.ChangePassword import ChangePassword
from AdminFirst.views.AdminSecondManagement import AdminSecondManagement
from AdminFirst.views.AdminThirdManagement import AdminThirdManagement
from AdminFirst.views.NoticeTemplateManagement import NoticeTemplateManagement
from AdminFirst.views.ActivityManagement import ActivityManagement
from AdminFirst.views.MerchandiseManagement import MerchandiseManagement
from AdminFirst.views.MerchandiseRequest import MerchandiseRequest

from utils.LogOut import admin_logout

app_name = 'AdminFirst'

urlpatterns = [
    # 管理员首页
    path('admin-index/', AdminIndex.as_view(), name='admin_index'),
    # 个人信息
    path('profile/', Profile.as_view(), name='profile'),
    # 修改密码
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    # 二级管理员管理
    path('admin-second-management/', AdminSecondManagement.as_view(), name='admin_second_management'),
    # 三级管理员管理
    path('admin-third-management/', AdminThirdManagement.as_view(), name='admin_third_management'),
    # 通知模板管理
    path('notice-template-management/', NoticeTemplateManagement.as_view(), name='notice_template_management'),
    # 活动管理
    path('activity-management/', ActivityManagement.as_view(), name='activity_management'),
    # 商品管理
    path('merchandise-management/', MerchandiseManagement.as_view(), name='merchandise_management'),
    # 商户请求
    path('merchandise-request/', MerchandiseRequest.as_view(), name='merchandise_request'),

    # 登出
    path('logout/', admin_logout, name='admin_logout'),
]
