from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib import messages

from AdminThird.models import AdminThird
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord
from Customer.models import Customer
from Notice.models import NoticeTemplate
from Address.models import Town

from utils.SendNotice import send_one
from utils.CheckExists import check_customer_phone_exists
from utils.login_checker import admin_third_login_required


class CustomerManagement(View):
    """ 客户管理
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
        # 获取此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取一开始要筛选的镇子、村子、组
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 判断是否有镇子，如果没有，则表示是第一次进入，还没选择地址范围
        # 引导客户管理-地址选择页面
        if not town:
            # 打包数据
            context = {
                'name': admin_third.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminThird/customer-management-select-address.html', context=context)

        # 如果是所有镇子，就重置为空字符串来实现筛选所有
        if town == '所有镇子':
            town = ''
        # 获取可能的筛选字段并筛选活动记录
        # 并且同时根据地址范围筛选
        filter_keyword = request.GET.get('filter_keyword', '')
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third=AdminThird.objects.get(job_num=request.session.get('job_num'))),
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword),
            Q(customer__town__contains=town),
            Q(customer__village__contains=village),
            Q(customer__group__contains=group)
        )

        # 获取所有通知模板，按发布时间逆序排序
        notice_templates = NoticeTemplate.objects.all().order_by('-create_time')

        # 打包可能存在的错误/成功信息
        # 未截止的活动，按创建时间倒序
        # 与当前三级管理员有关的活动参与记录，按报名时间倒序
        context = {
            'filter_keyword': filter_keyword,
            'activities': Activity.objects.filter(end_time__gte=datetime.now()).order_by('-create_time'),
            'activity_records': activity_records.order_by('-create_time'),
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'notice_templates': notice_templates,
            'town': town,
            'village': village,
            'group': group,
            'towns': Town.objects.all(),
        }
        return render(request, 'AdminThird/customer-management.html', context=context)

    @method_decorator(admin_third_login_required)
    def post(self, request):
        # 获取一开始的区域筛选信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')

        # 获取前端的动作
        # add 增加
        # change 修改
        # del 删除
        # change_tag 修改标签
        # send_notice 发送通知
        # change_comment 修改备注
        # merchant_comment 商户备注
        action = request.POST.get('action')
        if action == 'add':
            # 获取填写的用户信息
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            town_add = request.POST.get('town_add')
            village_add = request.POST.get('village_add')
            group_add = request.POST.get('group_add')
            street_add = request.POST.get('street_add')
            activity_id = request.POST.get('activity')

            # 判断此手机号是否已在客户数据库中
            # 没有就创建，有就直接取出
            if check_customer_phone_exists(phone):
                # 存在，直接取出
                customer = Customer.objects.get(phone=phone)
            else:
                # 不存在，创建
                customer = Customer.objects.create(
                    name=name,
                    gender=gender,
                    town=town_add,
                    village=village_add,
                    group=group_add,
                    street=street_add,
                    phone=phone,
                )

            # 判断此客户是否已经参加了此活动
            if ActivityRecord.objects.filter(activity_id=activity_id, customer_id=customer.id):
                # 已参加了此活动，记录客户已参加此活动错误
                request.session['error_message'] = '该客户已参加此活动！'
                # 重定向客户管理页面
                return redirect('AdminThird:customer_management')

            # 没问题了，创建记录
            ActivityRecord.objects.create(
                activity=Activity.objects.get(id=activity_id),
                customer=customer,
                admin_third=AdminThird.objects.get(job_num=request.session.get('job_num')),
            )
            # 记录成功信息并重定向客户管理页面
            request.session['success_message'] = '增加成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change':
            # 从前端获取要修改的信息
            change_id = request.POST.get('change_id')
            change_name = request.POST.get('change_name')
            change_gender = request.POST.get('change_gender')
            change_phone = request.POST.get('change_phone')
            change_town = request.POST.get('change_town')
            change_village = request.POST.get('change_village')
            change_group = request.POST.get('change_group')
            change_street = request.POST.get('change_street')

            # 取出该客户信息并进行修改
            customer = Customer.objects.get(id=change_id)
            customer.name = change_name
            customer.gender = change_gender
            customer.phone = change_phone
            customer.town = change_town
            customer.village = change_village
            customer.group = change_group
            customer.street = change_street
            customer.save()

            # 记录修改成功提示并重定向客户管理页面
            request.session['success_message'] = '信息修改成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'del':
            # 从前端获取要删除的记录id
            del_id = request.POST.get('del_id')

            # 从活动记录表中取出该条记录并删除
            activity_record = ActivityRecord.objects.get(id=del_id)
            activity_record.delete()

            # 记录删除成功信息并重定向客户管理页面
            request.session['success_message'] = '记录删除成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_tag':
            change_id = request.POST.get('change_id')
            change_tag = request.POST.get('change_tag')
            change_tag_type = request.POST.get('change_tag_type')
            # 取出客户并更改信息
            customer = Customer.objects.get(id=change_id)
            customer.tag = change_tag
            customer.tag_type = change_tag_type
            customer.save()
            # 记录成功信息并重定向客户管理页面
            request.session['success_message'] = '修改成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'send_notice':
            # 获取信息
            send_customer_id = request.POST.get('send_customer_id')
            notice_template_id = request.POST.get('notice_id')
            need_msg = request.POST.get('need_msg')

            # 推送通知
            send_one(send_customer_id, notice_template_id, need_msg)

            # 记录成功信息
            request.session['success_message'] = '通知发送成功'
            # 重定向客户管理页面
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
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
            # 重定向客户管理页面
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'merchant_comment':
            # 获取信息
            customer_id = request.POST.get('merchant_comment_customer_id')
            is_merchant = request.POST.get('is_merchant')
            is_installed_micro_post_pay = request.POST.get('is_installed_micro_post_pay')
            is_catering_merchant = request.POST.get('is_catering_merchant')
            salt_delivery = request.POST.get('salt_delivery')
            # 转换布尔值数据
            boolean_data_converter = {'0': False, '1': True, None: None}
            is_merchant = boolean_data_converter.get(is_merchant)
            is_installed_micro_post_pay = boolean_data_converter.get(is_installed_micro_post_pay)
            is_catering_merchant = boolean_data_converter.get(is_catering_merchant)

            # 取出该客户
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                # 未取到该客户
                messages.error(request, '未取到该客户')
                return redirect('AdminThird:customer_management')
            # 取到该客户了

            # 更新信息
            customer.is_merchant = is_merchant
            customer.is_installed_micro_post_pay = is_installed_micro_post_pay
            customer.is_catering_merchant = is_catering_merchant
            customer.salt_delivery = salt_delivery
            customer.save()

            # 记录成功信息
            messages.success(request, '更改成功')
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village,
                                                                                                  group)
            )
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )

