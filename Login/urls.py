from django.urls import path
from . import views

app_name = 'Login'

urlpatterns = [
    # 管理员登录
    path('admin-login/', views.AdminLogin.as_view(), name='admin_login'),
    # 客户登录
    path('customer-login/', views.CustomerLogin.as_view(), name='customer_login'),

    # 客户登录获取短信验证码
    path('customer-login-get-msg-code', views.get_msg_code, name='customer_login_get_msg_code'),
]