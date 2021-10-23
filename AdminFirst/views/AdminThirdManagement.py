from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django .views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib import messages

from AdminFirst.models import AdminFirst
from AdminSecond.models import AdminSecond
from AdminThird.models import AdminThird
from ActivitySignUp.models import ActivityRecord

from utils.GetMD5 import get_md5
from utils.CheckExists import check_job_num_exists
from utils.login_checker import admin_first_login_required


class AdminThirdManagement(View):
    """ 三级管理员管理
    """
    @method_decorator(admin_first_login_required)
    def get(self, request):
        # 取出此一级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字并筛选三级管理员
        filter_keyword = request.GET.get('filter_keyword', '')
        admin_thirds = AdminThird.objects.filter(
            Q(name__contains=filter_keyword) |
            Q(admin_second__name__contains=filter_keyword) |
            Q(job_num__contains=filter_keyword)
        )
        # 统计每个三级管理员总客户量以及今日客户量
        # 记录{
        #   'admin_third': 三级管理员,
        #   'total_customer_num': 总客户量,
        #   'today_customer_num': 今日客户量
        # }
        admin_thirds_customer_num = []
        for admin_third in admin_thirds:
            # 获取此三级管理员所有客户
            customers = ActivityRecord.objects.filter(admin_third=admin_third)
            # 统计总客户量
            total_customer_num = customers.count()
            # 获取今天日期并统计今日客户量
            today = datetime.today()
            today_customer_num = customers.filter(
                Q(create_time__year=today.year),
                Q(create_time__month=today.month),
                Q(create_time__day=today.day),
            ).count()
            # 记录到列表
            admin_thirds_customer_num.append({
                'admin_third': admin_third,
                'total_customer_num': total_customer_num,
                'today_customer_num': today_customer_num,
            })

        # 取出所有二级管理员
        admin_seconds = AdminSecond.objects.all()

        # 取出所有三级管理员
        admin_third_all = AdminThird.objects.all()

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'name': admin_first.name,
            'admin_thirds_customer_num': admin_thirds_customer_num,
            'admin_seconds': admin_seconds,
            'admin_third_all': admin_third_all,
        }
        return render(request, 'AdminFirst/admin-third-management.html', context=context)

    @method_decorator(admin_first_login_required)
    def post(self, request):
        # 获取action，并判断执行相应的操作
        # add 新增
        # del 删除
        # change_password 修改密码
        # change_admin_second 变更二级管理员
        # transfer_customer 转让名下客户
        action = request.POST.get('action')
        if action == 'add':
            # 获取新增信息
            name = request.POST.get('name')
            job_num = request.POST.get('job_num')
            password = get_md5(request.POST.get('password'))
            admin_second_id = request.POST.get('admin_second')

            # 判断给定工号是否已存在
            if check_job_num_exists(job_num):
                # 记录此工号已存在错误信息
                request.session['error_message'] = '此工号已存在'
                # 重定向三级管理员管理页面
                return redirect('AdminFirst:admin_third_management')

            # 新增
            AdminThird.objects.create(
                name=name,
                job_num=job_num,
                password=password,
                admin_second=AdminSecond.objects.get(id=admin_second_id),
            )

            # 记录成功信息
            request.session['success_message'] = '新增成功'
            # 重定向三级管理员管理页面
            return redirect('AdminFirst:admin_third_management')
        elif action == 'del':
            # 获取要删除的三级管理员id
            del_id = request.POST.get('del_id')
            # 取出要删除的三级管理员
            admin_third = AdminThird.objects.get(id=del_id)
            # 判断此三级管理员下是否还有客户
            # 有的话就报错不给删
            if admin_third.activityrecord_set.exists():
                # 记录该三级管理员还有客户未转出
                request.session['error_message'] = '该三级管理员还有未转出客户，请转出后再删除'
                # 重定向三级管理员管理页面
                return redirect('AdminFirst:admin_third_management')
            # 删除
            admin_third.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向三级管理员管理页面
            return redirect('AdminFirst:admin_third_management')
        elif action == 'change_password':
            # 获取要修改密码的三级管理员id和新密码
            change_id = request.POST.get('change_id')
            change_password = get_md5(request.POST.get('change_password'))

            # 取出并修改
            admin_third = AdminThird.objects.get(id=change_id)
            admin_third.password = change_password
            admin_third.save()

            # 记录成功信息
            request.session['success_message'] = '密码修改成功'
            # 重定向三级管理员管理页面
            return redirect('AdminFirst:admin_third_management')
        elif action == 'change_admin_second':
            # 获取要变更的三级管理员id以及变更的二级管理员id
            change_id = request.POST.get('change_id')
            change_admin_second_id = request.POST.get('change_admin_second')

            # 取出此三级管理员
            admin_third = AdminThird.objects.get(id=change_id)
            # 变更
            admin_third.admin_second = AdminSecond.objects.get(id=change_admin_second_id)
            admin_third.save()

            # 记录成功信息
            request.session['success_message'] = '变更成功'
            # 重定向三级管理员管理页面
            return redirect('AdminFirst:admin_third_management')
        elif action == 'transfer_customer':
            # 获取两个三级管理员的id
            from_admin_third_id = request.POST.get('transfer_customer_admin_third_id')
            to_admin_third_id = request.POST.get('transfer_admin_third')

            # 取出这两个三级管理员
            try:
                from_admin_third = AdminThird.objects.get(id=from_admin_third_id)
                to_admin_third = AdminThird.objects.get(id=to_admin_third_id)
            except AdminThird.DoesNotExist:
                # 未取到
                messages.error(request, '未取到该客户经理，请刷新重试')
                return redirect('AdminFirst:admin_third_management')
            # 取到这两个三级管理员了

            # 遍历将from名下的客户转移到to名下
            for customer_activity_record in from_admin_third.activityrecord_set.all():
                customer_activity_record.admin_third = to_admin_third
                customer_activity_record.save()
            # 转移完毕

            # 记录成功信息
            messages.success(request, '转让成功')
            return redirect('AdminFirst:admin_third_management')

        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向三级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminFirst:admin_third_management')

