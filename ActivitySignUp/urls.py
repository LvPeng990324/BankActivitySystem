from django.urls import path
from . import views
from . import apis

app_name = 'ActivitySignUp'

urlpatterns = [
    # 报名表
    path('activity-form/', views.ActivityForm.as_view(), name='activity_form'),
    # 活动信息
    path('activity-information/', views.ActivityInformation.as_view(), name='activity_information'),

    # 获取短信验证码接口
    path('get-msg-code/', views.get_msg_code, name='get_msg_code'),
    # 获取活动介绍接口
    path('get-activity-content/', apis.get_activity_content, name='get_activity_content'),
]