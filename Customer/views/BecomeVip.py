from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.utils.decorators import method_decorator

from Customer.models import Customer

from utils.CheckCardNum import check_card_num
from utils.login_checker import customer_login_required


class BecomeVip(View):
    """ 成为会员
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取出是否是vip
        is_vip = customer.is_vip

        # 取出可能有的邮政卡卡号
        card_num = customer.card_num

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': customer.name,
            'is_vip': is_vip,
            'card_num': card_num,
        }
        return render(request, 'Customer/become_vip.html', context=context)

    @method_decorator(customer_login_required)
    def post(self, request):
        # 获取输入的卡号
        card_num = request.POST.get('card_num')

        # 验证卡号有效性
        if not check_card_num(card_num):
            # 卡号不合法
            # 记录错误信息
            request.session['error_message'] = '卡号输入有误，请核查再次输入'
            # 重定向成为会员页面
            return redirect('Customer:become_vip')

        # 验证通过，记录该用户卡号
        # 取出该用户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))
        # 记录卡号
        customer.card_num = card_num
        # 设置为会员
        customer.is_vip = True
        # 保存
        customer.save()

        # 记录成功信息
        request.session['success_message'] = '卡号保存成功'

        # 重定向成为会员页面
        return redirect('Customer:become_vip')

