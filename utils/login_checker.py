# 是否登录检查器
from django.contrib import messages
from django.shortcuts import redirect


def admin_zero_login_required(func):
    """ 检查是否是零级管理员
    """
    def wrapper(request, *args, **kwargs):
        # 验证身份
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            messages.error(request, '登录已过期，重新登录')
            return redirect('Login:admin_login')
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper


def admin_first_login_required(func):
    """ 检查是否是一级管理员
    """
    def wrapper(request, *args, **kwargs):
        # 验证身份
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            messages.error(request, '登录已过期，重新登录')
            return redirect('Login:admin_login')
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper


def admin_second_login_required(func):
    """ 检查是否是二级管理员
    """
    def wrapper(request, *args, **kwargs):
        # 验证身份
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            messages.error(request, '登录已过期，重新登录')
            return redirect('Login:admin_login')
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper


def admin_third_login_required(func):
    """ 检查是否是三级管理员
    """
    def wrapper(request, *args, **kwargs):
        # 验证身份
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            messages.error(request, '登录已过期，重新登录')
            return redirect('Login:admin_login')
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper


def customer_login_required(func):
    """ 检查是否是客户
    """
    def wrapper(request, *args, **kwargs):
        # 验证身份
        if request.session.get('who_login') != 'Customer':
            request.session.flush()
            messages.error(request, '登录已过期，重新登录')
            return redirect('Login:customer_login')
        # 验证通过，放行
        return func(request, *args, **kwargs)
    return wrapper


