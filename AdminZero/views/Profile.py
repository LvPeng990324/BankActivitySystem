from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminZero.models import AdminZero

from utils.login_checker import admin_zero_login_required


class Profile(View):
    """ 个人信息
    """
    @method_decorator(admin_zero_login_required)
    def get(self, request):
        # 取出此零级管理员对象
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin_zero.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminZero/profile.html', context=context)

    @method_decorator(admin_zero_login_required)
    def post(self, request):
        # 暂时没啥能改的
        pass

