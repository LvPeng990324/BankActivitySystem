# 发送短信验证码
from django.http import HttpResponse
from django_redis import get_redis_connection

from utils.SendMessage import send_msg_code
from utils.GetRandomCode import get_random_code


def get_msg_code(request):
    # 获取要发送的手机号
    phone = request.GET.get('phone')
    # 获取随机验证码
    msg_code = get_random_code()
    # 记录到redis中
    redis_cli = get_redis_connection('msg_code')
    redis_cli.setex(phone, 60*5, msg_code)  # 设置5分钟过期
    # 发送短信
    res = send_msg_code(phone, msg_code)
    # 000000是官方的成功状态码
    # 其他错误码去容联云开发文档查阅
    if res.statusCode == '000000':
        return HttpResponse('success')
    else:
        return HttpResponse('短信发送错误码：' + res.statusCode)
