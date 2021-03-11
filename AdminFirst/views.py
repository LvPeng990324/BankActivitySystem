from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django .views import View
from datetime import datetime
from datetime import timedelta

from BankActivitySystem.settings import DEPLOY_DOMAIN
from Notice.models import NoticeTemplate
from .models import AdminFirst
from AdminSecond.models import AdminSecond
from AdminThird.models import AdminThird
from Customer.models import Customer
from ActivitySignUp.models import ActivityRecord
from ActivitySignUp.models import Activity

from utils.GetMD5 import get_md5
from utils.CheckExists import check_job_num_exists


class AdminIndex(View):
    """ 管理员首页
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此一级管理员
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 客户总数
        total_customer_num = ActivityRecord.objects.all().count()

        # 今日新增客户
        today = datetime.today()
        today_customer_num = ActivityRecord.objects.filter(
            Q(create_time__year=today.year),
            Q(create_time__month=today.month),
            Q(create_time__day=today.day)
        ).count()

        # 取出所有未删除的活动并按创建时间逆序排序
        recent_activities = Activity.objects.filter(is_delete=False).order_by('-create_time')

        # 近期10个活动
        recent_activities_10 = recent_activities[:10]

        # 近期活动客户量
        # 取出最近的7个活动信息
        recent_activities_7 = recent_activities[:7]
        # 记录活动名字并统计此次活动中的客户数量
        recent_activity_customer_num = []  # 记录{'activity_name': 活动名, 'customer_num': 客户数量}关系
        for activity in recent_activities_7:
            # 获取此次活动此二级管理员下所有三级管理员在这个活动中的客户数量以及此活动名字
            customer_num = activity.activityrecord_set.all().count()
            activity_name = activity.name
            # 记录到列表中
            recent_activity_customer_num.append({
                'activity_name': activity_name,
                'customer_num': customer_num,
            })

        # 近两周客户量趋势
        # 获取时间区间
        now_time = datetime.now()
        old_time = now_time - timedelta(weeks=2)
        # 把近两周的客户参与记录取出
        recent_activity_records = ActivityRecord.objects.filter(
            Q(create_time__gte=old_time),
            Q(create_time__lte=now_time),
        )
        # 获取时间区间内每一天的时间对象
        # 查询每天的客户量并记录到{'time': 时间, 'customer_num': 客户数量}关系中
        recent_day_customer_num = []
        for temp_day in range(15):
            # 获取这一天时间对象
            temp_old_time = now_time - timedelta(days=temp_day)
            # 查询这一天的客户数量
            customer_num = recent_activity_records.filter(
                Q(create_time__year=temp_old_time.year),
                Q(create_time__month=temp_old_time.month),
                Q(create_time__day=temp_old_time.day),
            ).count()
            # 记录到列表中
            recent_day_customer_num.append({
                'time': temp_old_time,
                'customer_num': customer_num,
            })

        # 打包信息
        context = {
            'name': admin_first.name,
            'job_num': request.session.get('job_num'),
            'total_customer_num': total_customer_num,
            'today_customer_num': today_customer_num,
            'recent_activities_10': recent_activities_10,
            'recent_activity_customer_num': recent_activity_customer_num[::-1],  # 为了图表好看，反转元素
            'recent_day_customer_num': recent_day_customer_num[::-1],  # 为了图表好看，反转元素
        }
        return render(request, 'AdminFirst/admin-index.html', context=context)


class Profile(View):
    """ 个人信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此一级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin_first.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminFirst/profile.html', context=context)

    def post(self, request):
        # 暂时没啥能改的
        pass


class ChangePassword(View):
    """ 修改密码
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 打包可能存在的错误/成功信息
        context = {
            'name': AdminFirst.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
        }
        return render(request, 'AdminFirst/change-password.html', context=context)

    def post(self, request):
        # 从前端取得填写的旧密码以及两次新密码
        old_password = get_md5((request.POST.get('old_password')))
        new_password = get_md5((request.POST.get('new_password')))
        confirm_password = get_md5((request.POST.get('confirm_password')))

        # 对比旧密码是否正确
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))
        current_password = admin_first.password
        if old_password != current_password:
            # 旧密码错误
            request.session['error_message'] = '旧密码有误！'
            return redirect('AdminFirst:change_password')
        # 对比两次确认密码是否一致
        if new_password != confirm_password:
            # 不一致错误
            request.session['error_message'] = '两次新密码不一致！'
            return redirect('AdminFirst:change_password')

        # 更新密码
        admin_first.password = new_password
        admin_first.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向密码更改页面
        return redirect('AdminFirst:change_password')


class AdminSecondManagement(View):
    """ 二级管理员管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此一级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

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
            'name': admin_first.name,
            'admin_seconds_customer_num': admin_seconds_customer_num,
        }
        return render(request, 'AdminFirst/admin-second-management.html', context=context)

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
                return redirect('AdminFirst:admin_second_management')

            # 新增
            AdminSecond.objects.create(
                name=name,
                job_num=job_num,
                password=password
            )
            # 记录成功信息
            request.session['success_message'] = '增加成功'
            # 重定向二级管理员管理页面
            return redirect('AdminFirst:admin_second_management')
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
            return redirect('AdminFirst:admin_second_management')
        elif action == 'del':
            # 获取要删除的二级管理员id
            del_id = request.POST.get('del_id')
            # 删除
            admin_second = AdminSecond.objects.get(id=del_id)
            admin_second.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向二级管理员管理页面
            return redirect('AdminFirst:admin_second_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向二级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminFirst:admin_second_management')


class AdminThirdManagement(View):
    """ 三级管理员管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

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

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'name': admin_first.name,
            'admin_thirds_customer_num': admin_thirds_customer_num,
            'admin_seconds': admin_seconds,
        }
        return render(request, 'AdminFirst/admin-third-management.html', context=context)

    def post(self, request):
        # 获取action，并判断执行相应的操作
        # add 新增
        # del 删除
        # change_password 修改密码
        # change_admin_second 变更二级管理员
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
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向三级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminFirst:admin_third_management')


class NoticeTemplateManagement(View):
    """ 客户通知模板管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此一级管理员
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键字筛选通知模板，并按发布时间逆序排序
        notice_templates = NoticeTemplate.objects.filter(
            Q(title__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': admin_first.name,
            'filter_keyword': filter_keyword,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminFirst/notice-template-management.html', context=context)

    def post(self, request):
        # 获取action并根据action执行不同操作
        # add 新增
        # change 更改
        # del 删除
        action = request.POST.get('action')
        if action == 'add':
            # 获取新增的信息
            title = request.POST.get('title')
            content = request.POST.get('content')
            # 新增
            NoticeTemplate.objects.create(
                title=title,
                content=content
            )
            # 记录成功信息
            request.session['success_message'] = '新增成功'
            # 重定向客户通知模板管理页面
            return redirect('AdminFirst:notice_template_management')
        elif action == 'change':
            # 获取要修改的信息
            change_id = request.POST.get('change_id')
            change_title = request.POST.get('change_title')
            change_content = request.POST.get('change_content')
            # 取出要修改的通知模板
            notice_template = NoticeTemplate.objects.get(id=change_id)
            notice_template.title = change_title
            notice_template.content = change_content
            notice_template.save()
            # 记录成功信息
            request.session['success_message'] = '修改成功'
            # 重定向客户通知模板管理页面
            return redirect('AdminFirst:notice_template_management')
        elif action == 'del':
            # 获取要删除的id
            del_id = request.POST.get('del_id')
            # 删除
            notice_template = NoticeTemplate.objects.get(id=del_id)
            notice_template.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向客户通知模板管理页面
            return redirect('AdminFirst:notice_template_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户通知模板管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminFirst:notice_template_management')


class ActivityManagement(View):
    """ 活动管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminFirst':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出此二级管理员对象
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 取出所有未删除的活动并按照时间逆序排序
        # 根据筛选关键字进行筛选
        activities = Activity.objects.filter(
            Q(is_delete=False),
            Q(name__contains=filter_keyword) |
            Q(admin_second__name__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包信息
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': admin_first.name,
            'filter_keyword': filter_keyword,
            'activities': activities,
            'domain': DEPLOY_DOMAIN,
        }
        return render(request, 'AdminFirst/activity-management.html', context=context)

    def post(self, request):
        # 获取动作并根据动作来执行相应的操作
        # del 删除活动
        action = request.POST.get('action')
        if action == 'del':
            del_id = request.POST.get('del_id')
            activity = Activity.objects.get(id=del_id)

            # 一级管理员有权限直接删除活动
            # 标记此活动已删除
            activity.is_delete = True
            activity.save()
            # 记录成功信息，并重定向活动管理页面
            request.session['success_message'] = '删除成功'
            return redirect('AdminFirst:activity_management')

        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向活动管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminFirst:activity_management')


