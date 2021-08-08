from django.shortcuts import render
from django.shortcuts import redirect
from django .views import View
from django.utils.decorators import method_decorator

from AdminFirst.models import AdminFirst

from utils.login_checker import admin_first_login_required


class Profile(View):
    """ 个人信息
    """
    @method_decorator(admin_first_login_required)
    def get(self, request):
        # 取出此一级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin_first.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminFirst/profile.html', context=context)

    @method_decorator(admin_first_login_required)
    def post(self, request):
        # 暂时没啥能改的
        pass

