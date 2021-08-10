from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages

from AdminSecond.models import AdminSecond
from ActivitySignUp.models import ActivityRecord
from AdminThird.models import AdminThird
from Customer.models import Customer
from Address.models import Town

from utils.login_checker import admin_second_login_required


class CustomerInformation(View):
    """ 客户信息
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 取出此二级管理员
        admin = AdminSecond.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取一开始要筛选的镇子、村子、组
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 判断是否有镇子，如果没有，则表示是第一次进入，还没选择地址范围
        # 引导客户管理-地址选择页面
        if not town:
            # 打包数据
            context = {
                'name': admin.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminSecond/customer-information-select-address.html', context=context)

        # 取出此二级管理员下所有三级管理员
        admin_thirds = AdminThird.objects.filter(admin_second=admin)

        # 如果是所有镇子，就重置为空字符串来实现筛选所有
        if town == '所有镇子':
            town = ''
        # 获取可能存在的筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 取出此二级管理员下所有三级管理员的所有客户参与信息，并按照创建时间逆序排序
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third__in=admin_thirds),
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
            'name': admin.name,
            'activity_records': activity_records,
            'filter_keyword': filter_keyword,
            'town': town,
            'village': village,
            'group': group,
            'admin_thirds': admin_thirds,
        }
        return render(request, 'AdminSecond/customer-information.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 获取一开始的区域筛选信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')

        # 根据action判断动作
        # change_tag 更改标签
        # change_comment 更改备注
        # change_admin_third 更改客户经理
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
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
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
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_admin_third':
            # 获取信息
            change_admin_third_activity_record_id = request.POST.get('change_admin_third_activity_record_id')
            change_admin_third_id = request.POST.get('change_admin_third')

            # 取出客户
            try:
                change_activity_record = ActivityRecord.objects.get(id=change_admin_third_activity_record_id)
            except Customer.DoesNotExist:
                # 未取到该客户
                messages.error(request, '未取到该客户')
                return redirect('AdminSecond:customer_information')
            # 取到该客户了

            # 取出该三级管理员
            try:
                change_admin_third = AdminThird.objects.get(id=change_admin_third_id)
            except AdminThird.DoesNotExist:
                # 未取到该客户经理
                messages.error(request, '未取到该客户经理')
                return redirect('AdminSecond:customer_information')
            # 取到该三级管理员了

            # 更改三级管理员
            change_activity_record.admin_third = change_admin_third
            change_activity_record.save()

            # 记录成功信息
            messages.success(request, '更改成功')
            return redirect(
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village,
                                                                                                    group)
            )
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户信息页面
            request.session['error_message'] = '非法操作类型'
            return redirect(
                reverse('AdminSecond:customer_information') + '?town={}&village={}&group={}'.format(town, village, group)
            )
