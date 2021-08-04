from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views import View
from datetime import datetime
from datetime import timedelta
from BankActivitySystem.settings import DEPLOY_DOMAIN

from AdminSecond.models import AdminSecond
from ActivitySignUp.models import ActivityRecord
from ActivitySignUp.models import Activity
from AdminThird.models import AdminThird
from Customer.models import Customer
from Notice.models import NoticeTemplate
from Address.models import Town

from utils.GetMD5 import get_md5


class AdminIndex(View):
    """ 二级管理员首页
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取此二级管理员对象
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 统计客户总数
        # 取出此二级管理员下的所有三级管理员
        admin_thirds = admin.adminthird_set.all()
        total_customer = ActivityRecord.objects.filter(admin_third__in=admin_thirds)
        total_customer_num = total_customer.count()

        # 统计今日新增客户
        # 获取今天
        now_time = datetime.now()
        # 筛选今天的记录并计数
        today_customer_num = total_customer.filter(
            create_time__year=now_time.year,
            create_time__month=now_time.month,
            create_time__day=now_time.day,
        ).count()

        # 取出所有未删除的活动并按创建时间逆序排序
        recent_activities = Activity.objects.filter(is_delete=False).order_by('-create_time')

        # 近期活动我部客户量
        # 取出最近的7个活动信息
        recent_activities_7 = recent_activities[:7]
        # 记录活动名字并统计该二级管理员下所有三级管理员在这个活动中的客户数量
        recent_activity_my_customer_num = []  # 记录{'activity_name': 活动名, 'customer_num': 客户数量}关系
        for activity in recent_activities_7:
            # 获取此次活动此二级管理员下所有三级管理员在这个活动中的客户数量以及此活动名字
            customer_num = activity.activityrecord_set.filter(admin_third__in=admin_thirds).count()
            activity_name = activity.name
            # 记录到列表中
            recent_activity_my_customer_num.append({
                'activity_name': activity_name,
                'customer_num': customer_num,
            })

        # 近两周我部客户量趋势
        # 获取时间区间
        now_time = datetime.now()
        old_time = now_time - timedelta(weeks=2)
        # 把近两周此二级管理员下所有三级管理员获得的客户参与记录取出
        recent_activity_records = ActivityRecord.objects.filter(
            Q(admin_third__in=admin_thirds),
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

        # 近期活动，选取最新的10条活动，按时间逆序
        recent_activities_10 = recent_activities[:10]

        # 打包数据
        context = {
            'name': admin.name,
            'job_num': request.session.get('job_num'),
            'total_customer_num': total_customer_num,
            'today_customer_num': today_customer_num,
            'recent_activity_my_customer_num': recent_activity_my_customer_num[::-1],  # 为了图表好看，把列表元素逆序
            'recent_day_customer_num': recent_day_customer_num[::-1],  # 为了图表好看，把列表元素逆序
            'recent_activities_10': recent_activities_10,
        }
        return render(request, 'AdminSecond/admin-index.html', context=context)


class Profile(View):
    """ 个人信息
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此二级管理员对象
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 打包数据
        context = {
            'name': admin.name,
            'job_num': request.session.get('job_num'),
        }
        return render(request, 'AdminSecond/profile.html', context=context)

    def post(self, request):
        # 暂时没啥能改的
        pass


class ChangePassword(View):
    """ 修改密码
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 打包可能存在的错误/成功信息
        context = {
            'name': AdminSecond.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
        }
        return render(request, 'AdminSecond/change-password.html', context=context)

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


class AdminThirdManagement(View):
    """ 三级管理员管理
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

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


class CustomerInformation(View):
    """ 客户信息
    """

    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此二级管理员
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取一开始要筛选的镇子、村子、组
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 判断是否有镇子，如果没有，则表示是第一次进入，还没选择地址范围
        # 引导客户管理-地址选择页面
        if not town:
            # 打包数据
            context = {
                'name': admin.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminSecond/customer-information-select-address.html', context=context)

        # 取出此二级管理员下所有三级管理员
        admin_thirds = AdminThird.objects.filter(admin_second=admin)

        # 如果是所有镇子，就重置为空字符串来实现筛选所有
        if town == '所有镇子':
            town = ''
        # 获取可能存在的筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 取出此二级管理员下所有三级管理员的所有客户参与信息，并按照创建时间逆序排序
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third__in=admin_thirds),
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword),
            Q(customer__town__contains=town),
            Q(customer__village__contains=village),
            Q(customer__group__contains=group)
        ).order_by('-create_time')

        # 打包信息
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': admin.name,
            'activity_records': activity_records,
            'filter_keyword': filter_keyword,
            'town': town,
            'village': village,
            'group': group,
        }
        return render(request, 'AdminSecond/customer-information.html', context=context)

    def post(self, request):
        # 获取一开始的区域筛选信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')

        # 根据action判断动作
        # change_tag 更改标签
        # change_comment 更改备注
        action = request.POST.get('action')
        if action == 'change_tag':
            # 获取要更改的客户id以及要更改的信息
            change_id = request.POST.get('change_id')
            change_tag = request.POST.get('change_tag')
            change_tag_type = request.POST.get('change_tag_type')
            # 更改并保存
            customer = Customer.objects.get(id=change_id)
            customer.tag = change_tag
            customer.tag_type = change_tag_type
            customer.save()
            # 记录成功信息并重定向客户信息页面
            request.session['success_message'] = '更改成功'
            return redirect(
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_comment':
            # 获取信息
            comment_customer_id = request.POST.get('comment_customer_id')
            customer_comment = request.POST.get('customer_comment')

            # 获取此客户
            customer = Customer.objects.get(id=comment_customer_id)
            # 修改备注信息
            customer.comment = customer_comment
            customer.save()

            # 记录成功信息
            request.session['success_message'] = '备注修改成功'
            return redirect(
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户信息页面
            request.session['error_message'] = '非法操作类型'
            return redirect(
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )


class ActivityManagement(View):
    """ 活动管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出此二级管理员对象
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

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
            'name': admin.name,
            'filter_keyword': filter_keyword,
            'activities': activities,
            'domain': DEPLOY_DOMAIN,
        }
        return render(request, 'AdminSecond/activity-management.html', context=context)

    def post(self, request):
        # 获取动作并根据动作来执行相应的操作
        # del 删除活动
        action = request.POST.get('action')
        if action == 'del':
            del_id = request.POST.get('del_id')
            activity = Activity.objects.get(id=del_id)
            # 检查此活动是否属于当前二级管理员或没有归属
            # 如果属于其他二级管理员则不允许删除
            if activity.admin_second:
                if activity.admin_second.job_num != request.session.get('job_num'):
                    # 记录无权删除错误信息
                    request.session['error_message'] = '只有发布者才可删除，您无权删除此活动'
                    # 重定向活动管理页面
                    return redirect('AdminSecond:activity_management')
            # 标记此活动已删除
            activity.is_delete = True
            activity.save()
            # 记录成功信息，并重定向活动管理页面
            request.session['success_message'] = '删除成功'
            return redirect('AdminSecond:activity_management')

        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向活动管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminSecond:activity_management')


class NoticeTemplateManagement(View):
    """ 客户通知模板管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminSecond':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此二级管理员
        admin_second = AdminSecond.objects.get(job_num=request.session.get('job_num'))

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
            'name': admin_second.name,
            'filter_keyword': filter_keyword,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminSecond/notice-template-management.html', context=context)

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
            return redirect('AdminSecond:notice_template_management')
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
            return redirect('AdminSecond:notice_template_management')
        elif action == 'del':
            # 获取要删除的id
            del_id = request.POST.get('del_id')
            # 删除
            notice_template = NoticeTemplate.objects.get(id=del_id)
            notice_template.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向客户通知模板管理页面
            return redirect('AdminSecond:notice_template_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户通知模板管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminSecond:notice_template_management')
