from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Q

from Merchandise.models import Merchandise

from utils.login_checker import admin_zero_login_required


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

        # 打包数据
        context = {
            'merchandises': merchandises,
            'filter_keyword': filter_keyword,
        }
        return render(request, 'AdminZero/merchandise-management.html', context=context)

