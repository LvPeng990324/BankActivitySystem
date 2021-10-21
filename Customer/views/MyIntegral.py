from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib import messages

from Customer.models import Customer
from Merchandise.models import Merchandise
from Merchandise.models import MerchandiseExchangeRecord

from utils.login_checker import customer_login_required


class MyIntegral(View):
    """ 我的积分
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出当前客户
        customer = Customer.objects.get(id=request.session.get('customer_id'))
        # 取出当前积分数量
        integral = customer.integral

        # 取出所有未删除的且库存量大于0的商品
        merchandises = Merchandise.objects.filter(
            is_delete=False,  # 要未删除的
            remain_num__gt=0,  # 要库存量大于0的
        )

        # 取出他的所有兑换记录
        merchandise_exchange_records = MerchandiseExchangeRecord.objects.filter(
            customer=customer,  # 要客户是他自己的
        ).order_by('-create_time')  # 根据创建时间逆序排序

        context = {
            'integral': integral,
            'merchandises': merchandises,
            'merchandise_exchange_records': merchandise_exchange_records,
        }
        return render(request, 'Customer/my-integral.html', context=context)

    @method_decorator(customer_login_required)
    def post(self, request):
        # 获取要兑换的商品id
        merchandise_id = request.POST.get('exchange_merchandise_id')
        # 取出该商品
        try:
            merchandise = Merchandise.objects.get(
                id=merchandise_id,
                is_delete=False,  # 要未删除的
                remain_num__gt=0,  # 要库存大于0的
            )
        except Merchandise.DoesNotExist:
            # 商品不存在或者已无库存
            messages.error(request, '上皮不存在或者已无库存')
            return redirect('Customer:my_integral')
        # 取到该商品了

        # 取出当前客户
        customer = Customer.objects.get(id=request.session.get('customer_id'))

        # 检查当前客户积分是否足够
        if customer.integral < merchandise.integral_price:
            # 积分不足
            messages.error(request, '你的积分不足，兑换失败')
            return redirect('Customer:my_integral')
        # 积分充足

        # 扣除积分
        customer.integral -= merchandise.integral_price
        customer.save()

        # 记录兑换请求
        new_merchandise_exchange_record = MerchandiseExchangeRecord.objects.create(
            merchandise=merchandise,
            customer=customer,
        )

        # 扣除商品库存
        merchandise.remain_num -= 1
        merchandise.save()

        # 返回成功信息
        messages.success(request, '兑换成功')
        return redirect('Customer:my_integral')


