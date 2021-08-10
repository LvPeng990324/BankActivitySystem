from django.urls import path
from Customer.views.CustomerIndex import CustomerIndex
from Customer.views.MyNotice import MyNotice
from Customer.views.NoticeDetail import NoticeDetail
from Customer.views.ProgressingActivity import ProgressingActivity
from Customer.views.ActivityDetail import ActivityDetail
from Customer.views.BecomeVip import BecomeVip
from Customer.views.ChangePassword import ChangePassword
from Customer.views.ReceivedMerchandise import ReceivedMerchandise

from Customer.apis.get_customer_comments import get_customer_comments

from utils.LogOut import customer_logout

app_name = 'Customer'

urlpatterns = [
    # 客户首页
    path('customer-index/', CustomerIndex.as_view(), name='customer_index'),
    # 我的通知
    path('my-notice/', MyNotice.as_view(), name='my_notice'),
    # 通知详情
    path('notice-detail/', NoticeDetail.as_view(), name='notice-detail'),
    # 进行中活动
    path('progressing-activity/', ProgressingActivity.as_view(), name='progressing_activity'),
    # 活动详情
    path('activity-detail/', ActivityDetail.as_view(), name='activity_detail'),
    # 成为会员
    path('become-vip/', BecomeVip.as_view(), name='become_vip'),
    # 更改密码
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    # 收到的礼品
    path('received-merchandise/', ReceivedMerchandise.as_view(), name='received_merchandise'),

    # 获取客户备注接口
    path('get-customer-comment/', get_customer_comments, name='get_customer_comment'),

    # 登出
    path('logout/', customer_logout, name='logout'),
]