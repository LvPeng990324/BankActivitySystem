from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect

from Merchandise.models import GiveMerchandiseRecord

from utils.login_checker import customer_login_required


class ReceivedMerchandise(View):
    """ 我的礼品
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出我收到的商品记录信息
        received_merchandise_records = GiveMerchandiseRecord.objects.filter(
            customer__phone=request.session.get('customer_phone'),
        )

        # 打包数据
        context = {
            'received_merchandise_records': received_merchandise_records,
        }
        return render(request, 'Customer/received-merchandise.html', context=context)


