from django.shortcuts import render
from django.shortcuts import redirect
from django .views import View

from AdminFirst.models import AdminFirst


class Profile(View):
    """ 个人信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此一级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin_first.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminFirst/profile.html', context=context)

    def post(self, request):
        # 暂时没啥能改的
        pass

