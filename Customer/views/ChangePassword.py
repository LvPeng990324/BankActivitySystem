from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from Customer.models import Customer

from utils.GetMD5 import get_md5


class ChangePassword(View):
    """ 更改密码
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': customer.name,
        }
        return render(request, 'Customer/change-password.html', context=context)

    def post(self, request):
        # 获取输入的两次密码
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # 如果两次密码不一致则返回两次密码不一致错误
        if new_password != confirm_password:
            request.session['error_message'] = '两次密码不一致，请重试'
            return redirect('Customer:change_password')

        # 转换为md5并记录
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))
        customer.password = get_md5(new_password)
        customer.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向客户密码更改页面
        return redirect('Customer:change_password')



