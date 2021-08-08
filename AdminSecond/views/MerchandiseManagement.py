from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages

from Merchandise.models import Merchandise
from AdminThird.models import AdminThird
from Customer.models import Customer
from Merchandise.models import GiveMerchandiseRecord

from utils.login_checker import admin_second_login_required


class MerchandiseManagement(View):
    """ 商品管理
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):
        # 获取筛选关键词
        filter_word = request.GET.get('filter_word', '')

        # 取出所有未删除的商品
        merchandises = Merchandise.objects.filter(
            is_delete=False
        )

        # 如果有筛选关键词就筛选
        if filter_word:
            merchandises = merchandises.filter(
                Q(name__icontains=filter_word)  # 筛选商品名
            )

        # 取出该二级管理员下的所有三级管理员
        admin_thirds = AdminThird.objects.filter(admin_second__job_num=request.session.get('job_num'))
        # 取出这些三级管理员的客户们
        customers = Customer.objects.filter(activityrecord__admin_third__in=admin_thirds)

        # 打包数据
        context = {
            'merchandises': merchandises,
            'filter_word': filter_word,
            'customers': customers,
        }
        return render(request, 'AdminSecond/merchandise-management.html', context=context)

    @method_decorator(admin_second_login_required)
    def post(self, request):
        # 获取action
        action = request.POST.get('action')
        # 根据action进行响应的动作
        # add_merchandise 新增商品
        # change_merchandise 修改商品
        # give_merchandise 修改商品
        # delete_merchandise 删除商品
        if action == 'add_merchandise':
            return add_merchandise_action(request)
        elif action == 'change_merchandise':
            return change_merchandise_action(request)
        elif action == 'give_merchandise':
            return give_merchandise_action(request)
        elif action == 'delete_merchandise':
            return delete_merchandise_action(request)
        else:
            messages.error(request, '未定义的动作，请重试')
            return redirect('AdminSecond:merchandise_management')


def add_merchandise_action(request):
    """ 新增商品动作
    """
    # 获取信息
    add_name = request.POST.get('name')
    add_remain_num = request.POST.get('remain_num')
    add_description = request.POST.get('description')

    # 新增商品
    Merchandise.objects.create(
        name=add_name,
        remain_num=add_remain_num,
        description=add_description,
    )

    # 记录成功信息
    messages.success(request, '新增成功')
    return redirect('AdminSecond:merchandise_management')


def change_merchandise_action(request):
    """ 修改商品动作
    """
    # 获取信息
    change_id = request.POST.get('change_id')
    change_name = request.POST.get('change_name')
    change_remain_num = request.POST.get('change_remain_num')
    change_description = request.POST.get('change_description')

    # 取出要修改的商品
    try:
        merchandise = Merchandise.objects.get(id=change_id)
    except Merchandise.DoesNotExist:
        # 未取到该商品
        messages.error(request, '未取到该商品')
        return redirect('AdminSecond:merchandise_management')
    # 取到该商品了

    # 修改信息
    merchandise.name = change_name
    merchandise.remain_num = change_remain_num
    merchandise.description = change_description
    merchandise.save()

    # 记录成功信息
    messages.success(request, '修改成功')
    return redirect('AdminSecond:merchandise_management')


def give_merchandise_action(request):
    """ 发放商品动作
    """
    # 获取信息
    merchandise_id = request.POST.get('give_id')
    customer_id = request.POST.get('give_customer')
    give_num = int(request.POST.get('give_num'))

    # 取出该商品
    try:
        merchandise = Merchandise.objects.get(id=merchandise_id)
    except Merchandise.DoesNotExist:
        # 未取到该商品
        messages.error(request, '未取到该商品')
        return redirect('AdminSecond:merchandise_management')
    # 取到该商品了

    # 取出该客户
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        # 未取到该客户
        messages.error(request, '未取到该客户')
        return redirect('AdminSecond:merchandise_management')
    # 取到该客户了

    # 判断该商品库存够不够
    if merchandise.remain_num < give_num:
        # 库存不足
        messages.error(request, '库存不足，发放失败')
        return redirect('AdminSecond:merchandise_management')
    # 可以发放了

    # 记录该客户发放记录
    GiveMerchandiseRecord.objects.create(
        merchandise=merchandise,
        customer=customer,
        give_num=give_num,
        give_admin_name=request.session.get('name'),
    )

    # 扣除该商品的库存
    merchandise.remain_num -= give_num
    merchandise.save()

    # 记录成功信息
    messages.success(request, '发放成功')
    return redirect('AdminSecond:merchandise_management')


def delete_merchandise_action(request):
    """ 删除商品动作
    """
    # 获取要删除的id
    delete_id = request.POST.get('delete_id')

    # 取出要删除的商品
    try:
        merchandise = Merchandise.objects.get(id=delete_id)
    except Merchandise.DoesNotExist:
        # 未取到该商品
        messages.error(request, '未取到该商品')
        return redirect('AdminSecond:merchandise_management')
    # 取到该商品了

    # 标记为删除状态
    merchandise.is_delete = True
    merchandise.save()

    # 记录成功信息
    messages.success(request, '删除成功')
    return redirect('AdminSecond:merchandise_management')



