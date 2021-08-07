from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from Customer.models import Customer
from ActivitySignUp.models import Activity


class ActivityDetail(View):
    """ 活动详情
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

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

