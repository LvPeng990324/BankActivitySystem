from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminThird.models import AdminThird


class Profile(View):
    """ 个人信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出个人信息
        job_num = request.session.get('job_num')
        name = AdminThird.objects.get(job_num=job_num)

        # 打包信息
        context = {
            'job_num': job_num,
            'name': name,
        }
        return render(request, 'AdminThird/profile.html', context=context)

    def post(self, request):
        # 暂时没有什么可以改的
        pass

