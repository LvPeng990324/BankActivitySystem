from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator

from Customer.models import Customer
from ActivitySignUp.models import Activity

from utils.login_checker import customer_login_required


class ProgressingActivity(View):
    """ 进行中活动
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取得过滤关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键字筛选进行中的活动，并按发布时间逆序排序
        now_time = datetime.now()
        progressing_activities = Activity.objects.filter(
            Q(is_delete=False),
            Q(end_time__gte=now_time),
            Q(name__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'name': customer.name,
            'filter_keyword': filter_keyword,
            'progressing_activities': progressing_activities,
        }
        return render(request, 'Customer/progressing_activity.html', context=context)

