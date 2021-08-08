from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminThird.models import AdminThird
from Notice.models import NoticeTemplate

from utils.login_checker import admin_third_login_required


class NoticeView(View):
    """ 通知查看
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
        # 验证登录身份
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键字筛选通知模板，并根据创建时间逆序排序
        notice_templates = NoticeTemplate.objects.filter(
            Q(title__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'filter_keyword': filter_keyword,
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminThird/notice-view.html', context=context)

