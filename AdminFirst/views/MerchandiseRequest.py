from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator

from RequestAction.models import RequestAction
from RequestAction.models import RequestActionLog
from AdminThird.models import AdminThird

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

        context = {
            'request_actions': request_actions,
            'pending_request_action_logs': pending_request_action_logs,
            'finished_request_action_logs': finished_request_action_logs,
        }
        return render(request, 'AdminFirst/merchandise_request.html', context=context)



