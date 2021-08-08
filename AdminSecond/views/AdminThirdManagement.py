from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator

from AdminSecond.models import AdminSecond
from ActivitySignUp.models import ActivityRecord
from AdminThird.models import AdminThird

from utils.GetMD5 import get_md5
from utils.login_checker import admin_second_login_required


class AdminThirdManagement(View):
    """ 三级管理员管理
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 获取模糊搜索关键字
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出此二级管理员
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 取出此二级管理员下的所有三级管理员并按照模糊搜索关键字进行筛选
        admin_thirds = AdminThird.objects.filter(
            Q(admin_second=admin),
            Q(name__contains=filter_keyword),
        )
        # 统计每个三级管理员今日的客户量以及总客户量
        # 记录{'admin_third': 三级管理员, 'total_customer_num': 总客户量, 'today_customer_num': 今日客户量}关系
        admin_thirds_customer_num = []
        for admin_third in admin_thirds:
            today = datetime.today()
            total_customer = ActivityRecord.objects.filter(admin_third=admin_third)
            total_customer_num = total_customer.count()
            today_customer_num = total_customer.filter(
                Q(create_time__year=today.year),
                Q(create_time__month=today.month),
                Q(create_time__day=today.day),
            ).count()
            admin_thirds_customer_num.append({
                'admin_third': admin_third,
                'total_customer_num': total_customer_num,
                'today_customer_num': today_customer_num,
            })

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': admin.name,
            'filter_keyword': filter_keyword,
            'admin_thirds': admin_thirds,
            'admin_thirds_customer_num': admin_thirds_customer_num
        }
        return render(request, 'AdminSecond/admin-third-management.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 获取前端的动作
        # change_password 修改三级管理员密码
        action = request.POST.get('action')
        # 判断要执行的操作
        if action == 'change_password':
            # 修改三级管理员密码
            # 获取新密码并md5加密
            change_password = get_md5(request.POST.get('change_password'))
            # 获取要更改的三级管理员id
            change_id = request.POST.get('change_id')
            # 更改保存
            admin_third = AdminThird.objects.get(id=change_id)
            admin_third.password = change_password
            admin_third.save()
            # 记录成功信息并重定向三级管理员页面
            request.session['success_message'] = '密码修改成功'
            return redirect('AdminSecond:admin_third_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向三级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminSecond:admin_third_management')
