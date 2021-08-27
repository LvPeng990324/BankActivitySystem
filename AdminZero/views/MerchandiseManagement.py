from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages

from Merchandise.models import Merchandise
from Merchandise.models import GiveMerchandiseRecord

from utils.login_checker import admin_zero_login_required
from utils.ExportExcel import export_give_merchandise_record


class MerchandiseManagement(View):
    """ 商品管理
    """
    @method_decorator(admin_zero_login_required)
    def get(self, request):
        # 获取筛选关键词
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出所有未删除的商品
        merchandises = Merchandise.objects.filter(
            is_delete=False
        )

        # 如果有筛选关键词就筛选
        if filter_keyword:
            merchandises = merchandises.filter(
                Q(name__icontains=filter_keyword)  # 筛选商品名
            )

        # 获取所有的商品发放记录并按照发放时间逆序排序
        give_merchandise_records = GiveMerchandiseRecord.objects.all().order_by('-give_time')

        # 打包数据
        context = {
            'merchandises': merchandises,
            'filter_keyword': filter_keyword,
            'give_merchandise_records': give_merchandise_records,
        }
        return render(request, 'AdminZero/merchandise-management.html', context=context)

    @method_decorator(admin_zero_login_required)
    def post(self, request):
        # 获取action
        action = request.POST.get('action')
        # 根据action进行响应的动作
        # export_give_merchandise_record 导出商品发放记录表
        if action == 'export_give_merchandise_record':
            return export_give_merchandise_record_action(request)
        else:
            messages.error(request, '未定义的动作，请重试')
            return redirect('AdminZero:merchandise_management')

def export_give_merchandise_record_action(request):
    """ 导出商品发放记录表
    """
    # 获取所有的商品发放记录并按照发放时间逆序排序
    give_merchandise_records = GiveMerchandiseRecord.objects.all().order_by('-give_time')

    # 导出Excel
    return export_give_merchandise_record(data=give_merchandise_records)
