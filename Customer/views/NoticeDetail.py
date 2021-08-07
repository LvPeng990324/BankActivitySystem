from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from Customer.models import Customer
from Notice.models import Notice


class NoticeDetail(View):
    """ 通知详情
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取出要查看详情的通知
        notice_id = request.GET.get('notice_id')
        notice = Notice.objects.get(id=notice_id)

        # 标记此条通知为已读状态
        notice.is_read = True
        notice.save()

        # 打包数据
        context = {
            'name': customer.name,
            'notice': notice
        }
        return render(request, 'Customer/notice-detail.html', context=context)
