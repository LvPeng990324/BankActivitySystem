from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminSecond.models import AdminSecond

from utils.GetMD5 import get_md5
from utils.login_checker import admin_second_login_required


class ChangePassword(View):
    """ 修改密码
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 打包可能存在的错误/成功信息
        context = {
            'name': AdminSecond.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
        }
        return render(request, 'AdminSecond/change-password.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 从前端取得填写的旧密码以及两次新密码
        old_password = get_md5((request.POST.get('old_password')))
        new_password = get_md5((request.POST.get('new_password')))
        confirm_password = get_md5((request.POST.get('confirm_password')))

        # 对比旧密码是否正确
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))
        current_password = admin.password
        if old_password != current_password:
            # 旧密码错误
            request.session['error_message'] = '旧密码有误！'
            return redirect('AdminSecond:change_password')
        # 对比两次确认密码是否一致
        if new_password != confirm_password:
            # 不一致错误
            request.session['error_message'] = '两次新密码不一致！'
            return redirect('AdminSecond:change_password')

        # 更新密码
        admin.password = new_password
        admin.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向密码更改页面
        return redirect('AdminSecond:change_password')
