from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from BankActivitySystem.settings import DEPLOY_DOMAIN
from django.utils.decorators import method_decorator

from AdminSecond.models import AdminSecond
from ActivitySignUp.models import Activity

from utils.login_checker import admin_second_login_required


class ActivityManagement(View):
    """ 活动管理
    """
    @method_decorator(admin_second_login_required)
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

    @method_decorator(admin_second_login_required)
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
