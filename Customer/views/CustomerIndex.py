from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator

from Customer.models import Customer
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord
from Notice.models import Notice

from utils.login_checker import customer_login_required


class CustomerIndex(View):
    """ 客户首页
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取出所有未删除和未截止活动，按发布时间逆序排序
        now_time = datetime.now()
        activities = Activity.objects.filter(
            Q(is_delete=False),
            Q(end_time__gte=now_time)
        ).order_by('-create_time')

        # 取出此客户参与的活动记录，按报名时间逆序排序
        activity_records = ActivityRecord.objects.filter(customer=customer).order_by('-create_time')

        # 统计参与活动数量
        my_activity_num = activity_records.count()
        # 统计进行中活动数量
        progressing_activity_num = activities.count()
        # 统计未读消息数量
        unread_notice_num = Notice.objects.filter(
            Q(customer=customer),
            Q(is_read=False)
        ).count()

        # 取出是否是会员
        is_vip = customer.is_vip
        # 取出标签内容
        tag = customer.tag

        # 打包数据
        context = {
            'name': customer.name,
            'activities': activities,
            'activity_records': activity_records,
            'my_activity_num': my_activity_num,
            'progressing_activity_num': progressing_activity_num,
            'unread_notice_num': unread_notice_num,
            'is_vip': is_vip,
            'tag': tag,
        }
        return render(request, 'Customer/customer-index.html', context=context)

