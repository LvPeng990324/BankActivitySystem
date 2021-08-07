from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminZero.models import AdminZero


class Profile(View):
    """ 个人信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此零级管理员对象
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin_zero.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminZero/profile.html', context=context)

    def post(self, request):
        # 暂时没啥能改的
        pass

