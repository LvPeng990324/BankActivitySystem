from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator

from Customer.models import Customer
from Notice.models import Notice

from utils.login_checker import customer_login_required


class MyNotice(View):
    """ 我的通知
    """
    @method_decorator(customer_login_required)
    def get(self, request):
        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 获取搜索关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 取出此客户所有通知，按关键字筛选并按照时间顺序逆序排序
        notices = Notice.objects.filter(
            Q(customer=customer),
            Q(title__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'name': customer.name,
            'filter_keyword': filter_keyword,
            'notices': notices,
        }
        return render(request, 'Customer/my-notice.html', context=context)

