from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminZero.models import AdminZero

from utils.GetMD5 import get_md5


class ChangePassword(View):
    """ 修改密码
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            return redirect('Login:admin_login')

        # 打包可能存在的错误/成功信息
        context = {
            'name': AdminZero.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
        }
        return render(request, 'AdminZero/change-password.html', context=context)

    def post(self, request):
        # 从前端取得填写的旧密码以及两次新密码
        old_password = get_md5((request.POST.get('old_password')))
        new_password = get_md5((request.POST.get('new_password')))
        confirm_password = get_md5((request.POST.get('confirm_password')))

        # 对比旧密码是否正确
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))
        current_password = admin_zero.password
        if old_password != current_password:
            # 旧密码错误
            request.session['error_message'] = '旧密码有误！'
            return redirect('AdminZero:change_password')
        # 对比两次确认密码是否一致
        if new_password != confirm_password:
            # 不一致错误
            request.session['error_message'] = '两次新密码不一致！'
            return redirect('AdminZero:change_password')

        # 更新密码
        admin_zero.password = new_password
        admin_zero.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向密码更改页面
        return redirect('AdminZero:change_password')

