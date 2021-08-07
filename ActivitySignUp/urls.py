from django.urls import path
from ActivitySignUp.views.ActivityForm import ActivityForm
from ActivitySignUp.views.ActivityInformation import ActivityInformation
from ActivitySignUp.apis.get_msg_code import get_msg_code
from ActivitySignUp.apis.get_activity_content import get_activity_content

app_name = 'ActivitySignUp'

urlpatterns = [
    # 报名表
    path('activity-form/', ActivityForm.as_view(), name='activity_form'),
    # 活动信息
    path('activity-information/', ActivityInformation.as_view(), name='activity_information'),

    # 获取短信验证码接口
    path('get-msg-code/', get_msg_code, name='get_msg_code'),
    # 获取活动介绍接口
    path('get-activity-content/', get_activity_content, name='get_activity_content'),
]