from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from AdminZero.models import AdminZero
from Notice.models import NoticeTemplate
from utils.login_checker import admin_zero_login_required


class NoticeTemplateManagement(View):
    """ 客户通知模板管理
    """
    @method_decorator(admin_zero_login_required)
    def get(self, request):
        # 取出此零级管理员
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

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
            'name': admin_zero.name,
            'filter_keyword': filter_keyword,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminZero/notice-template-management.html', context=context)

    @method_decorator(admin_zero_login_required)
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
            return redirect('AdminZero:notice_template_management')
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
            return redirect('AdminZero:notice_template_management')
        elif action == 'del':
            # 获取要删除的id
            del_id = request.POST.get('del_id')
            # 删除
            notice_template = NoticeTemplate.objects.get(id=del_id)
            notice_template.delete()
            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向客户通知模板管理页面
            return redirect('AdminZero:notice_template_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户通知模板管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminZero:notice_template_management')


