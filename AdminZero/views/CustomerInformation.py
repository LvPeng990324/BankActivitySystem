from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views import View

from AdminZero.models import AdminZero
from ActivitySignUp.models import ActivityRecord
from Customer.models import Customer
from Address.models import Town


class CustomerInformation(View):
    """ 客户信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此零级管理员
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取一开始要筛选的镇子、村子、组
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 判断是否有镇子，如果没有，则表示是第一次进入，还没选择地址范围
        # 引导客户管理-地址选择页面
        if not town:
            # 打包数据
            context = {
                'name': admin_zero.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminZero/customer-information-select-address.html', context=context)

        # 如果是所有镇子，就重置为空字符串来实现筛选所有
        if town == '所有镇子':
            town = ''
        # 获取可能存在的筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 筛选客户参与记录，并按照创建时间逆序排序
        activity_records = ActivityRecord.objects.filter(
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword),
            Q(customer__town__contains=town),
            Q(customer__village__contains=village),
            Q(customer__group__contains=group)
        ).order_by('-create_time')

        # 打包信息
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': admin_zero.name,
            'activity_records': activity_records,
            'filter_keyword': filter_keyword,
            'town': town,
            'village': village,
            'group': group,
        }
        return render(request, 'AdminZero/customer-information.html', context=context)

    def post(self, request):
        # 获取一开始的区域筛选信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')

        # 根据action判断动作
        # change_tag 更改标签
        # change_comment 更改备注
        action = request.POST.get('action')
        if action == 'change_tag':
            # 获取要更改的客户id以及要更改的信息
            change_id = request.POST.get('change_id')
            change_tag = request.POST.get('change_tag')
            change_tag_type = request.POST.get('change_tag_type')
            # 更改并保存
            customer = Customer.objects.get(id=change_id)
            customer.tag = change_tag
            customer.tag_type = change_tag_type
            customer.save()
            # 记录成功信息并重定向客户信息页面
            request.session['success_message'] = '更改成功'
            return redirect(
                reverse('AdminZero:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_comment':
            # 获取信息
            comment_customer_id = request.POST.get('comment_customer_id')
            customer_comment = request.POST.get('customer_comment')

            # 获取此客户
            customer = Customer.objects.get(id=comment_customer_id)
            # 修改备注信息
            customer.comment = customer_comment
            customer.save()

            # 记录成功信息
            request.session['success_message'] = '备注修改成功'
            return redirect(
                reverse('AdminZero:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户信息页面
            request.session['error_message'] = '非法操作类型'
            return redirect(
                reverse('AdminZero:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )

