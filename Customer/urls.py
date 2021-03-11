from django.urls import path
from . import views
from . import apis

from utils.LogOut import customer_logout

app_name = 'Customer'

urlpatterns = [
    # 客户首页
    path('customer-index/', views.CustomerIndex.as_view(), name='customer_index'),
    # 我的通知
    path('my-notice/', views.MyNotice.as_view(), name='my_notice'),
    # 通知详情
    path('notice-detail/', views.NoticeDetail.as_view(), name='notice-detail'),
    # 进行中活动
    path('progressing-activity/', views.ProgressingActivity.as_view(), name='progressing_activity'),
    # 活动详情
    path('activity-detail/', views.ActivityDetail.as_view(), name='activity_detail'),
    # 成为会员
    path('become-vip/', views.BecomeVip.as_view(), name='become_vip'),
    # 更改密码
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),

    # 获取客户备注接口
    path('get-customer-comment/', apis.get_customer_comments, name='get_customer_comment'),

    # 登出
    path('logout/', customer_logout, name='logout'),
]