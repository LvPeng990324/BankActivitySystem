from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import datetime

from Merchandise.models import MerchandiseExchangeRecord
from AdminThird.models import AdminThird

from utils.login_checker import admin_third_login_required


class MerchandiseExchange(View):
    """ 商品兑换
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
        # 取出当前三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))
        # 取出当前三级管理员下的所有客户的商品兑换记录
        merchandise_exchange_records = MerchandiseExchangeRecord.objects.filter(
            customer__activityrecord__admin_third=admin_third,  # 要客户经理是当前三级管理员的
        ).order_by('-create_time')  # 根据创建时间逆序排序

        # 将兑换记录分为已兑换和待兑换
        finished_merchandise_exchange_records = merchandise_exchange_records.filter(is_exchanged=True)  # 已兑换的
        pending_merchandise_exchange_records = merchandise_exchange_records.filter(is_exchanged=False)  # 待兑换的

        context = {
            'finished_merchandise_exchange_records': finished_merchandise_exchange_records,
            'pending_merchandise_exchange_records': pending_merchandise_exchange_records,
        }
        return render(request, 'AdminThird/merchandise-exchange.html', context=context)

    @method_decorator(admin_third_login_required)
    def post(self, request):
        # 获取要标记兑换完成的商品兑换记录id
        merchandise_exchange_record_id = request.POST.get('merchandise_exchange_record_id')
        # 取出该记录
        try:
            merchandise_exchange_record = MerchandiseExchangeRecord.objects.get(id=merchandise_exchange_record_id)
        except MerchandiseExchangeRecord.DoesNotExist:
            # 未取到该记录
            messages.error(request, '未取到该记录，请刷新重试')
            return redirect('AdminThird:merchandise_exchange')
        # 取到该记录了

        # 标记为已兑换并且记录兑换完成时间
        merchandise_exchange_record.is_exchanged = True
        merchandise_exchange_record.exchanged_time = datetime.datetime.now()
        merchandise_exchange_record.save()

        # 记录成功信息
        messages.success(request, '操作成功')
        return redirect('AdminThird:merchandise_exchange')

