from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.views import View
from datetime import datetime
from BankActivitySystem.settings import DEPLOY_DOMAIN

from AdminThird.models import AdminThird
from ActivitySignUp.models import Activity
from Address.models import Town

from utils.QRCode import get_qrcode_stream


class GenerateQRCode(View):
    """ 活动二维码
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取可能有的筛选字段并筛选活动信息
        filter_keyword = request.GET.get('filter_keyword', '')
        activities = Activity.objects.filter(
            Q(name__contains=filter_keyword),
        )

        # 获取所有镇子信息
        towns = Town.objects.all()

        # 打包信息
        context = {
            'name': AdminThird.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'activities': activities,
            'towns': towns,
        }
        return render(request, 'AdminThird/generate-qrcode.html', context=context)

    def post(self, request):
        # 获取要生成二维码的活动id
        activity_id = request.POST.get('activity_id')

        # 判断此活动是否已截止
        end_time = Activity.objects.get(id=activity_id).end_time
        now_time = datetime.now()
        if end_time < now_time:
            return HttpResponse('<h1>此活动已截止，不可报名</h1>')

        # 记录此三级管理员工号
        job_num = request.session.get('job_num')
        # 获取可能选择的地址信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')
        # 组合生成二维码需要的URL
        # 127.0.0.1:8000/activity-sign-up/activity-information/?job_num=0001&activity_id=3&town=城关镇&village=北关社区&group=1组
        qrcode_url = '{domain}/activity-sign-up/activity-information/?job_num={job_num}&activity_id={activity_id}&town={town}&village={village}&group={group}'.format(
            domain=DEPLOY_DOMAIN,
            job_num=job_num,
            activity_id=activity_id,
            town=town,
            village=village,
            group=group,
        )
        # 生成IO流的二维码数据
        qrcode_stream = get_qrcode_stream(qrcode_url)
        # 显示二维码
        return HttpResponse(qrcode_stream, content_type='image/png')

