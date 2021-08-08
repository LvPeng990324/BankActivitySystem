from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from Customer.models import Customer
from ActivitySignUp.models import Activity

from utils.login_checker import customer_login_required


class ActivityDetail(View):
    """ 活动详情
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 获得要查看详情的活动id
        activity_id = request.GET.get('activity_id')

        # 取出该活动
        activity = Activity.objects.get(id=activity_id)

        # 打包数据
        context = {
            'name': customer.name,
            'activity': activity,
        }
        return render(request, 'Customer/activity-detail.html', context=context)

