from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from django_redis import get_redis_connection
from django.contrib import auth


from AdminThird.models import AdminThird
from AdminSecond.models import AdminSecond
from AdminFirst.models import AdminFirst
from AdminZero.models import AdminZero
from Customer.models import Customer

from utils.GetMD5 import get_md5
from utils.GetRandomCode import get_random_code
from utils.SendMessage import send_msg_code


class AdminLogin(View):
    """ 管理员登录类
    """
    def get(self, request):
        # 判断是否已登录，如果已登录，判断登录身份来引导不同页面
        # 未登录就清除session并继续
        if request.session.get('who_login') == 'AdminZero':
            # 零级管理员
            return redirect('AdminZero:admin_index')
        elif request.session.get('who_login') == 'AdminFirst':
            # 一级管理员
            return redirect('AdminFirst:admin_index')
        elif request.session.get('who_login') == 'AdminSecond':
            # 二级管理员
            return redirect('AdminSecond:admin_index')
        elif request.session.get('who_login') == 'AdminThird':
            # 三级管理员
            return redirect('AdminThird:admin_index')
        else:
            # 打包可能存在的错误信息
            # 如果有错误信息就打包并清除在session的记录
            context = {
                'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            }
            # 未登录，清除session
            request.session.flush()
            # 引导管理员登录页面
            return render(request, 'Login/admin-login.html', context=context)

    def post(self, request):
        # 获取工号和密码
        job_num = request.POST.get('job_num')
        password = request.POST.get('password')
        # 获取md5加密后的密码
        password_md5 = get_md5(password)

        # 根据工号从零一二三管理员里取，并判断管理员的身份
        if AdminZero.objects.filter(job_num=job_num).exists():
            # 记录是零级管理员
            # 同时登录Django-admin的对应二级管理员账户，用于使用Django-ckeditor对活动进行编辑
            request.session['who_login'] = 'AdminZero'
            admin = AdminZero.objects.get(job_num=job_num)
            # 登录Django-admin
            django_admin_username = 'admin_second'
            django_admin_password = 'LVpeng-990324'
            django_admin_user_obj = auth.authenticate(username=django_admin_username, password=django_admin_password)
            auth.login(request, django_admin_user_obj)
        elif AdminFirst.objects.filter(job_num=job_num).exists():
            # 记录是一级管理员
            # 同时登录Django-admin的对应二级管理员账户，用于使用Django-ckeditor对活动进行编辑
            request.session['who_login'] = 'AdminFirst'
            admin = AdminFirst.objects.get(job_num=job_num)
            # 登录Django-admin
            django_admin_username = 'admin_second'
            django_admin_password = 'LVpeng-990324'
            django_admin_user_obj = auth.authenticate(username=django_admin_username, password=django_admin_password)
            auth.login(request, django_admin_user_obj)
        elif AdminSecond.objects.filter(job_num=job_num).exists():
            # 记录是二级管理员
            # 同时登录Django-admin的对应二级管理员账户，用于使用Django-ckeditor对活动进行编辑
            request.session['who_login'] = 'AdminSecond'
            admin = AdminSecond.objects.get(job_num=job_num)
            # 登录Django-admin
            django_admin_username = 'admin_second'
            django_admin_password = 'LVpeng-990324'
            django_admin_user_obj = auth.authenticate(username=django_admin_username, password=django_admin_password)
            auth.login(request, django_admin_user_obj)
        elif AdminThird.objects.filter(job_num=job_num).exists():
            # 记录是三级管理员
            request.session['who_login'] = 'AdminThird'
            admin = AdminThird.objects.get(job_num=job_num)
        else:
            # 工号不存在
            # 记录错误信息
            request.session['error_message'] = '工号不存在'
            # 重定向登录页面
            return redirect('Login:admin_login')

        # 判断密码是否正确
        if password_md5 != admin.password:
            # 密码错误
            # 清空登录者身份记录
            request.session['who_login'] = ''
            # 记录错误信息
            request.session['error_message'] = '密码错误'
            # 重定向登录页面
            return redirect('Login:admin_login')

        # 记录登录成功
        request.session['is_login'] = True
        request.session['job_num'] = job_num
        # 重定向登录页面
        return redirect('Login:admin_login')


class CustomerLogin(View):
    """ 客户登录类
    """
    def get(self, request):
        # 判断是否已登陆
        # 未登录或者登录身份不是客户，清除session记录并引导客户登录页面
        if not request.session.get('who_login') == 'Customer':
            context = {
                'error_message': request.session.get('error_message'),
            }
            request.session.flush()
            return render(request, 'Login/customer-login.html', context=context)

        # 看来是已经登录的客户了
        # 再次判断记录的手机号是否存在，避免被删除的客户登录出错
        if not Customer.objects.filter(phone=request.session.get('customer_phone')).exists():
            # 清除session记录
            request.session.flush()
            # 记录登录状态有误错误信息
            request.session['error_message'] = '登录状态有误，请重新登录'
            # 重定向客户登录页面
            return redirect('Login:customer_login')

        # 没问题了，转向客户后台首页
        return redirect('Customer:customer_index')

    def post(self, request):
        # 获取填写的手机号
        phone = request.POST.get('phone')
        # 看看用户记录里有没有这个手机号
        # 没有的话就记录此手机号无记录错误
        if not Customer.objects.filter(phone=phone).exists():
            # 记录此手机号无记录错误
            request.session['error_message'] = '此手机号无记录'
            # 重定向客户登录页面
            return redirect('Login:customer_login')

        # 获取用户登录的方法
        action = request.POST.get('action')
        # 判断不同的登录方法
        # msg_login 短信验证码登录
        # password_login 密码登录
        if action == 'msg_login':
            # 短信验证码登录
            # 获取填写的短信验证码
            msg_code = request.POST.get('msg_code')

            # 从redis取出此手机号的短信验证码
            redis_cli = get_redis_connection('msg_code')
            correct_msg_code = redis_cli.get(phone)  # 取出来是b数据，需要解码
            # 如果redis中有记录才进行解码操作，避免对None进行decode而报错
            if correct_msg_code:
                correct_msg_code = correct_msg_code.decode()

            # 验证短信验证码
            if msg_code != correct_msg_code:
                # 记录验证码错误错误信息
                request.session['error_message'] = '短信验证码有误'
                # 重定向客户登录页面
                return redirect('Login:customer_login')
        elif action == 'password_login':
            # 密码登录
            # 获取填写的密码并转为md5
            password = get_md5(request.POST.get('password'))
            # 取出正确的密码
            password_currect = Customer.objects.get(phone=phone).password
            # 进行密码比对，错误就记录错误信息并重定向客户登录页面
            if password_currect != password:
                request.session['error_message'] = '密码输入有误'
                return redirect('Login:customer_login')
        else:
            # 未知方法
            # 记录未知登录方法并重定向客户登录页面
            request.session['error_message'] = '未知的登录方法，请重试'
            return redirect('Login:customer_login')

        # 没问题了，记录登录信息
        request.session['who_login'] = 'Customer'
        request.session['customer_phone'] = phone

        # 重定向客户登录页面，将会根据记录的登录信息自动跳转相应的页面
        return redirect('Login:customer_login')


def get_msg_code(request):
    # 获取要发送的手机号
    phone = request.GET.get('phone')
    # 获取随机验证码
    msg_code = get_random_code()
    # 记录到redis中
    redis_cli = get_redis_connection('msg_code')
    redis_cli.setex(phone, 60 * 5, msg_code)  # 设置5分钟过期
    # 发送短信
    res = send_msg_code(phone, msg_code)
    # 000000是官方的成功状态码
    # 其他错误码去容联云开发文档查阅
    if res.statusCode == '000000':
        return HttpResponse('success')
    else:
        return HttpResponse('短信发送错误码：' + res.statusCode)
