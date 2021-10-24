from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from Customer.models import Customer
from Customer.models import IntegralGiveLog
from AdminThird.models import AdminThird

from utils.login_checker import admin_third_login_required


class GiveIntegral(View):
    """ 发放积分
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
        # 取出当前三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 取出当前三级管理员下的客户们
        customers = Customer.objects.filter(
            activityrecord__admin_third=admin_third,
        )

        # 取出这些客户的积分发放记录
        integral_give_logs = IntegralGiveLog.objects.filter(
            customer__in=customers,
        ).order_by('-create_time')  # 按照创建时间逆序排序

        context = {
            'integral_give_logs': integral_give_logs,
        }
        return render(request, 'AdminThird/give-integral.html', context=context)

    @method_decorator(admin_third_login_required)
    def post(self, request):
        # 获取信息
        give_customer_id = request.POST.get('give_customer')
        give_num = request.POST.get('give_num')

        # 取出当前三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 取出该客户
        try:
            customer = Customer.objects.get(id=give_customer_id)
        except Customer.DoesNotExist:
            # 未取到该客户
            messages.error(request, '未取到该客户，请刷新重试')
            return redirect('AdminThird:give_integral')
        # 取到该客户了

        # 增加积分
        customer.integral += int(give_num)
        customer.save()

        # 创建积分发放记录
        IntegralGiveLog.objects.create(
            customer=customer,
            admin_name=admin_third.name,
            give_num=give_num,
        )

        # 记录成功信息
        messages.success(request, '发放成功')
        return redirect('AdminThird:give_integral')

