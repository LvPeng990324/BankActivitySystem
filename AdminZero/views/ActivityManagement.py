from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminZero.models import AdminZero
from ActivitySignUp.models import Activity
from BankActivitySystem.settings import DEPLOY_DOMAIN


class ActivityManagement(View):
    """ 活动管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出此零级管理员对象
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

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
            'name': admin_zero.name,
            'filter_keyword': filter_keyword,
            'activities': activities,
            'domain': DEPLOY_DOMAIN,
        }
        return render(request, 'AdminZero/activity-management.html', context=context)

    def post(self, request):
        # 获取动作并根据动作来执行相应的操作
        # del 删除活动
        action = request.POST.get('action')
        if action == 'del':
            del_id = request.POST.get('del_id')
            activity = Activity.objects.get(id=del_id)

            # 拥有至高权利的零级管理员可以删除
            # 标记此活动已删除
            activity.is_delete = True
            activity.save()
            # 记录成功信息，并重定向活动管理页面
            request.session['success_message'] = '删除成功'
            return redirect('AdminZero:activity_management')

        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向活动管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminSecond:activity_management')

