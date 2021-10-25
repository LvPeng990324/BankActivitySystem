from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
import datetime

from RequestAction.models import RequestAction
from RequestAction.models import RequestActionLog
from AdminThird.models import AdminThird

from utils.login_checker import admin_second_login_required
from utils.DateUtils import check_date_in_range


class MerchandiseRequest(View):
    """ 商户请求
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 取出所有的商户请求动作
        request_actions = RequestAction.objects.all()

        # 取出当前二级管理下的所有三级管理
        admin_thirds = AdminThird.objects.filter(
            admin_second__job_num=request.session.get('job_num'),
        )

        # 取出当前用户相关的商户请求
        request_action_logs = RequestActionLog.objects.filter(
            customer__activityrecord__admin_third__in=admin_thirds,
        )

        # 将请求分为待处理和已完成
        pending_request_action_logs = request_action_logs.filter(is_finished=False)
        finished_request_action_logs = request_action_logs.filter(is_finished=True)

        context = {
            'request_actions': request_actions,
            'pending_request_action_logs': pending_request_action_logs,
            'finished_request_action_logs': finished_request_action_logs,
        }
        return render(request, 'AdminSecond/merchandise_request.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 获取action
        action = request.POST.get('action')
        # 根据action进行动作
        if action == 'confirm_finished':
            return confirm_finished_action(request)
        elif action == 'delete_request_action':
            return delete_request_action_action(request)
        elif action == 'add_request_action':
            return add_request_action_action(request)
        else:
            messages.error(request, '未定义的动作，请重试')
            return redirect('AdminSecond:merchandise_request')


def confirm_finished_action(request):
    """ 确认完成动作
    """
    # 获取要记录完成的请求记录id
    request_action_log_id = request.POST.get('request_action_log_id')

    # 取出该请求记录
    try:
        request_action_log = RequestActionLog.objects.get(id=request_action_log_id)
    except RequestActionLog.DoesNotExist:
        # 未取到该请求记录
        messages.error(request, '未取到该请求记录，请重试')
        return redirect('AdminSecond:merchandise_request')
    # 取到该请求记录了

    # 判断是否限制了起止日期
    if request_action_log.start_date and request_action_log.end_date:
        # 判断是否在起止日期段内
        if not check_date_in_range(start_date=request_action_log.start_date, end_date=request_action_log.end_date):
            # 不在日期段内
            messages.error(request, '当前不在起止日期段内，不可以执行该操作')
            return redirect('AdminSecond:merchandise_request')

    # 标记为已完成并记录完成时间
    request_action_log.is_finished = True
    request_action_log.finished_time = datetime.datetime.now()
    request_action_log.save()

    # 返回成功信息
    messages.success(request, '标记完成成功')
    return redirect('AdminSecond:merchandise_request')


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
        return redirect('AdminSecond:merchandise_request')
    # 取到该请求动作了

    # 删除
    delete_request_action.delete()

    # 记录成功信息
    messages.success(request, '删除成功')
    return redirect('AdminSecond:merchandise_request')


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
    return redirect('AdminSecond:merchandise_request')
