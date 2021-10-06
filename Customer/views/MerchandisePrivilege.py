from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from RequestAction.models import RequestAction
from RequestAction.models import RequestActionLog
from Customer.models import Customer

from utils.login_checker import customer_login_required
from utils.LogOut import customer_logout


class MerchandisePrivilege(View):
    """ 商户特权
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出所有请求动作
        request_actions = RequestAction.objects.all()
        # 取出当前客户的所有请求记录
        request_action_logs = RequestActionLog.objects.filter(
            customer__phone=request.session.get('customer_phone'),
        )

        # 打包数据
        context = {
            'request_actions': request_actions,
            'request_action_logs': request_action_logs,
        }
        return render(request, 'Customer/merchandise-privilege.html', context=context)

    @method_decorator(customer_login_required)
    def post(self, request):
        # 获取信息
        request_action_id = request.POST.get('request_action')
        remark = request.POST.get('remark')

        # 取出当前客户
        try:
            customer = Customer.objects.get(id=request.session.get('customer_id'))
        except Customer.DoesNotExist:
            # 未取到该客户
            messages.error(request, '登录已失效')
            return customer_logout(request)
        # 取到当前客户了

        # 取出该请求动作
        try:
            request_action = RequestAction.objects.get(id=request_action_id)
        except RequestAction.DoesNotExist:
            # 未取到该请求动作
            messages.error(request, '未取到该请求动作')
            return redirect('Customer:merchandise_privilege')
        # 取到该请求动作了

        # 创建请求记录
        new_request_action_log = RequestActionLog.objects.create(
            customer=customer,
            name=request_action.name,
            remark=remark,
        )

        # 记录成功信息
        messages.success(request, '请求成功')
        return redirect('Customer:merchandise_privilege')



