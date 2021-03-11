# 用户登出方法
from django.shortcuts import redirect


def admin_logout(request):
    request.session.flush()
    return redirect('Login:admin_login')


def customer_logout(request):
    request.session.flush()
    return redirect('Login:customer_login')
