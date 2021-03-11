from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.views import View
from datetime import datetime

from Customer.models import Customer
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord
from Notice.models import Notice

from utils.CheckCardNum import check_card_num
from utils.GetMD5 import get_md5


class CustomerIndex(View):
    """ 客户首页
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取出所有未删除和未截止活动，按发布时间逆序排序
        now_time = datetime.now()
        activities = Activity.objects.filter(
            Q(is_delete=False),
            Q(end_time__gte=now_time)
        ).order_by('-create_time')

        # 取出此客户参与的活动记录，按报名时间逆序排序
        activity_records = ActivityRecord.objects.filter(customer=customer).order_by('-create_time')

        # 统计参与活动数量
        my_activity_num = activity_records.count()
        # 统计进行中活动数量
        progressing_activity_num = activities.count()
        # 统计未读消息数量
        unread_notice_num = Notice.objects.filter(
            Q(customer=customer),
            Q(is_read=False)
        ).count()

        # 取出是否是会员
        is_vip = customer.is_vip
        # 取出标签内容
        tag = customer.tag

        # 打包数据
        context = {
            'name': customer.name,
            'activities': activities,
            'activity_records': activity_records,
            'my_activity_num': my_activity_num,
            'progressing_activity_num': progressing_activity_num,
            'unread_notice_num': unread_notice_num,
            'is_vip': is_vip,
            'tag': tag,
        }
        return render(request, 'Customer/customer-index.html', context=context)


class MyNotice(View):
    """ 我的通知
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

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


class ProgressingActivity(View):
    """ 进行中活动
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 取得过滤关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键字筛选进行中的活动，并按发布时间逆序排序
        now_time = datetime.now()
        progressing_activities = Activity.objects.filter(
            Q(is_delete=False),
            Q(end_time__gte=now_time),
            Q(name__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'name': customer.name,
            'filter_keyword': filter_keyword,
            'progressing_activities': progressing_activities,
        }
        return render(request, 'Customer/progressing_activity.html', context=context)


class ActivityDetail(View):
    """ 活动详情
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 获得要查看详情的活动id
        activity_id = request.GET.get('activity_id')

        # 取出该活动
        activity = Activity.objects.get(id=activity_id)

        # 打包数据
        context = {
            'name': customer.name,
            'activity': activity,
        }
        return render(request, 'Customer/activity-detail.html', context=context)


class BecomeVip(View):
    """ 成为会员
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

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


class ChangePassword(View):
    """ 更改密码
    """
    def get(self, request):
        # 检查登录状态
        if not request.session.get('who_login') == 'Customer':
            request.session.flush()
            return redirect('Login:customer_login')

        # 取出此客户
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'name': customer.name,
        }
        return render(request, 'Customer/change-password.html', context=context)

    def post(self, request):
        # 获取输入的两次密码
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # 如果两次密码不一致则返回两次密码不一致错误
        if new_password != confirm_password:
            request.session['error_message'] = '两次密码不一致，请重试'
            return redirect('Customer:change_password')

        # 转换为md5并记录
        customer = Customer.objects.get(phone=request.session.get('customer_phone'))
        customer.password = get_md5(new_password)
        customer.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向客户密码更改页面
        return redirect('Customer:change_password')



