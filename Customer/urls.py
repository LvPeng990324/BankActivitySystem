from django.urls import path
from Customer.views.CustomerIndex import CustomerIndex
from Customer.views.MyNotice import MyNotice
from Customer.views.NoticeDetail import NoticeDetail
from Customer.views.ProgressingActivity import ProgressingActivity
from Customer.views.ActivityDetail import ActivityDetail
from Customer.views.BecomeVip import BecomeVip
from Customer.views.ChangePassword import ChangePassword
from Customer.views.ReceivedMerchandise import ReceivedMerchandise
from Customer.views.MerchandisePrivilege import MerchandisePrivilege
from Customer.views.MyIntegral import MyIntegral

from Customer.apis.get_customer_comments import get_customer_comments
from Customer.apis.get_customer_by_phone import get_customer_by_phone

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
    # 商户特权
    path('merchandise-privilege/', MerchandisePrivilege.as_view(), name='merchandise_privilege'),
    # 我的积分
    path('my-integral/', MyIntegral.as_view(), name='my_integral'),

    # 获取客户备注接口
    path('get-customer-comment/', get_customer_comments, name='get_customer_comment'),
    # 通过手机号获取客户信息
    path('get-customer-by-phone/', get_customer_by_phone, name='get_customer_by_phone'),

    # 登出
    path('logout/', customer_logout, name='logout'),
]