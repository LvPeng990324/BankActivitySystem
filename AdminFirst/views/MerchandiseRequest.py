from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib import messages

from RequestAction.models import RequestAction
from RequestAction.models import RequestActionLog
from AdminThird.models import AdminThird
from Customer.models import Customer

from utils.login_checker import admin_first_login_required


class MerchandiseRequest(View):
    """ 商户请求
    """
    @method_decorator(admin_first_login_required)
    def get(self, request):
        # 取出所有的商户请求动作
        request_actions = RequestAction.objects.all()

        # 取出所有的商户请求
        request_action_logs = RequestActionLog.objects.all()

        # 将请求分为待处理和已完成
        pending_request_action_logs = request_action_logs.filter(is_finished=False)
        finished_request_action_logs = request_action_logs.filter(is_finished=True)

        # 取出所有商户客户
        merchandises = Customer.objects.filter(
            is_merchant=True,  # 要是商户的
        )

        context = {
            'request_actions': request_actions,
            'pending_request_action_logs': pending_request_action_logs,
            'finished_request_action_logs': finished_request_action_logs,
            'merchandises': merchandises,
        }
        return render(request, 'AdminFirst/merchandise_request.html', context=context)

    def post(self, request):
        # 获取action
        action = request.POST.get('action')
        # 根据action进行动作
        if action == 'send_request_action':
            return send_request_action_action(request)
        elif action == 'delete_request_action':
            return delete_request_action_action(request)
        elif action == 'add_request_action':
            return add_request_action_action(request)
        else:
            messages.error(request, '未定义的动作，请重试')
            return redirect('AdminFirst:merchandise_request')


def send_request_action_action(request):
    """ 发放任务动作
    """
    # 获取信息
    request_action_id = request.POST.get('request_action')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    target_merchandise_id_list = request.POST.getlist('target_merchandise')

    # 取出该请求动作
    try:
        request_action = RequestAction.objects.get(id=request_action_id)
    except RequestAction.DoesNotExist:
        # 未取到该请求动作
        messages.error(request, '该任务不存在')
        return redirect('AdminFirst:merchandise_request')
    # 取到该请求动作了

    # 取出这些选中的目标商户客户
    target_merchandise_list = []
    for target_merchandise_id in target_merchandise_id_list:
        # 尝试
        try:
            target_merchandise = Customer.objects.get(id=target_merchandise_id, is_merchant=True)
            target_merchandise_list.append(target_merchandise)
        except Customer.DoesNotExist:
            # 未取到目标商户客户
            messages.error(request, '所选商户有无效的，请刷新页面重试')

    # 批量创建任务
    for target_merchandise in target_merchandise_list:
        RequestActionLog.objects.create(
            customer=target_merchandise,
            name=request_action.name,
            start_date=start_date,
            end_date=end_date,
        )

    # 返回成功信息
    messages.success(request, '任务发放成功')
    return redirect('AdminFirst:merchandise_request')


def delete_request_action_action(request):
    """ 删除请求动作动作
    """
    # 获取要删除的请求动作id
    delete_request_action_id = request.POST.get('delete_request_action_id')

    # 取出该动作
    try:
        delete_request_action = RequestAction.objects.get(id=delete_request_action_id)
    except RequestAction.DoesNotExist:
        # 未取到该动作
        messages.error(request, '未取到该请求动作')
        return redirect('AdminFirst:merchandise_request')
    # 取到该请求动作了

    # 删除
    delete_request_action.delete()

    # 记录成功信息
    messages.success(request, '删除成功')
    return redirect('AdminFirst:merchandise_request')


def add_request_action_action(request):
    """ 新增请求动作动作
    """
    # 获取信息
    new_name = request.POST.get('new_name')

    # 创建动作
    RequestAction.objects.create(
        name=new_name,
    )

    # 记录成功信息
    messages.success(request, '新增成功')
    return redirect('AdminFirst:merchandise_request')




