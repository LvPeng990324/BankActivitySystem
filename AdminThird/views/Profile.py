from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminThird.models import AdminThird

from utils.login_checker import admin_third_login_required


class Profile(View):
    """ 个人信息
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
        # 取出个人信息
        job_num = request.session.get('job_num')
        name = AdminThird.objects.get(job_num=job_num)

        # 打包信息
        context = {
            'job_num': job_num,
            'name': name,
        }
        return render(request, 'AdminThird/profile.html', context=context)

    @method_decorator(admin_third_login_required)
    def post(self, request):
        # 暂时没有什么可以改的
        pass

