from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator

from AdminZero.models import AdminZero
from AdminSecond.models import AdminSecond
from AdminThird.models import AdminThird
from ActivitySignUp.models import ActivityRecord

from utils.GetMD5 import get_md5
from utils.CheckExists import check_job_num_exists
from utils.login_checker import admin_zero_login_required


class AdminSecondManagement(View):
    """ 二级管理员管理
    """
    @method_decorator(admin_zero_login_required)
    def get(self, request):
        # 取出此一级管理员对象
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字，并根据关键字筛选二级管理员
        filter_keyword = request.GET.get('filter_keyword', '')
        admin_seconds = AdminSecond.objects.filter(
            Q(name__contains=filter_keyword) |
            Q(job_num__contains=filter_keyword)
        )

        # 统计每个二级管理员的三级管理员数、总客户量以及今日客户量
        # 记录{
        #     'admin_second': 二级管理员,
        #     'admin_third_num'： 二级管理员数,
        #     'total_customer_num': 总客户量,
        #     'today_customer_num': 今日客户量
        # }关系
        admin_seconds_customer_num = []
        for admin_second in admin_seconds:
            # 取出此二级下的所有三级
            admin_thirds = AdminThird.objects.filter(admin_second=admin_second)
            # 统计三级管理员数
            admin_third_num = admin_thirds.count()
            # 取出这些三级的客户们（报名记录）
            customers = ActivityRecord.objects.filter(admin_third__in=admin_thirds)
            # 统计客户总量
            total_customer_num = customers.count()
            # 获取今天时间，用于统计今日客户量
            today = datetime.today()
            # 统计今日客户量
            today_customer_num = customers.filter(
                Q(create_time__year=today.year),
                Q(create_time__month=today.month),
                Q(create_time__day=today.day),
            ).count()
            # 记录到列表
            admin_seconds_customer_num.append({
                'admin_second': admin_second,
                'admin_third_num': admin_third_num,
                'total_customer_num': total_customer_num,
                'today_customer_num': today_customer_num,
            })

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'name': admin_zero.name,
            'admin_seconds_customer_num': admin_seconds_customer_num,
        }
        return render(request, 'AdminZero/admin-second-management.html', context=context)

    @method_decorator(admin_zero_login_required)
    def post(self, request):
        # 根据action判断动作
        # add 新增
        # del 删除
        # change_password 修改密码
        action = request.POST.get('action')
        if action == 'add':
            # 获取填写的信息
            name = request.POST.get('name')
            job_num = request.POST.get('job_num')
            password = get_md5(request.POST.get('password'))

            # 判断此工号是否已存在
            if check_job_num_exists(job_num):
                # 记录此工号的管理员已存在错误信息
                request.session['error_message'] = '此工号的管理员已存在'
                # 重定向到二级管理员管理页面
                return redirect('AdminZero:admin_second_management')

            # 新增
            AdminSecond.objects.create(
                name=name,
                job_num=job_num,
                password=password
            )
            # 记录成功信息
            request.session['success_message'] = '增加成功'
            # 重定向二级管理员管理页面
            return redirect('AdminZero:admin_second_management')
        elif action == 'change_password':
            # 获取要修改的二级管理员id以及新密码
            change_id = request.POST.get('change_id')
            change_password = get_md5(request.POST.get('change_password'))

            # 取出此二级管理员
            admin_second = AdminSecond.objects.get(id=change_id)
            admin_second.password = change_password
            admin_second.save()

            # 记录成功信息
            request.session['success_message'] = '密码修改成功'
            # 重定向二级管理员管理页面
            return redirect('AdminZero:admin_second_management')
        elif action == 'del':
            # 获取要删除的二级管理员id
            del_id = request.POST.get('del_id')
            # 删除
            admin_second = AdminSecond.objects.get(id=del_id)
            admin_second.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向二级管理员管理页面
            return redirect('AdminZero:admin_second_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向二级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminZero:admin_second_management')

