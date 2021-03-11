# 模版过滤器
from django.template import Library
from datetime import datetime

# 将注册类实例化为register对象
register = Library()


# TODO 活动状态判断
@register.filter
def if_out_of_date(end_time):
    now_time = datetime.now()
    print(end_time)
    print(now_time)
    if end_time > now_time:
        print('进行中')
        return '进行中'
    else:
        print('已截止')
        return '已截止'

