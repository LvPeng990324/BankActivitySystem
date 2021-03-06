from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminSecond.models import AdminSecond

from utils.login_checker import admin_second_login_required


class Profile(View):
    """ 个人信息
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此二级管理员对象
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminSecond/profile.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 暂时没啥能改的
        pass
