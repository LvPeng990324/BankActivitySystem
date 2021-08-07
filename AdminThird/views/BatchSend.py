from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminThird.models import AdminThird
from ActivitySignUp.models import ActivityRecord
from Notice.models import NoticeTemplate

from utils.SendNotice import batch_send


class BatchSend(View):
    """ 批量推送
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键词
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键词筛选客户参与记录
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third=AdminThird.objects.get(job_num=request.session.get('job_num'))),
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__town__contains=filter_keyword) |
            Q(customer__village__contains=filter_keyword) |
            Q(customer__group__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword)
        )

        # 获取所有通知模板，按发布时间逆序排序
        notice_templates = NoticeTemplate.objects.all().order_by('-create_time')

        # 打包数据
        context = {
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'activity_records': activity_records,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminThird/batch-send.html', context=context)

    def post(self, request):
        # 获取信息
        send_customer_ids = request.POST.get('send_customer_ids')
        notice_id = request.POST.get('notice_id')
        need_msg = request.POST.get('need_msg')

        # 推送通知
        batch_send(send_customer_ids, notice_id, need_msg)

        # 记录成功信息
        request.session['success_message'] = '通知推送成功'
        # 重定向批量推送页面
        return redirect('AdminThird:batch_send')


