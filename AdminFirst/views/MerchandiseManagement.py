from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages

from Merchandise.models import Merchandise

from utils.login_checker import admin_first_login_required


class MerchandiseManagement(View):
    """ 商品管理
    """
    @method_decorator(admin_first_login_required)
    def get(self, request):
        # 获取筛选关键词
        filter_keyword = request.GET.get('filter_keyword', '')

        # 取出所有未删除的商品
        merchandises = Merchandise.objects.filter(
            is_delete=False
        )

        # 如果有筛选关键词就筛选
        if filter_keyword:
            merchandises = merchandises.filter(
                Q(name__icontains=filter_keyword)  # 筛选商品名
            )

        # 打包数据
        context = {
            'merchandises': merchandises,
            'filter_keyword': filter_keyword,
        }
        return render(request, 'AdminFirst/merchandise-management.html', context=context)

    @method_decorator(admin_first_login_required)
    def post(self, request):
        # 获取action
        action = request.POST.get('action')
        # 根据action进行响应的动作
        # add_merchandise 新增商品
        # change_merchandise 修改商品
        # delete_merchandise 删除商品
        if action == 'add_merchandise':
            return add_merchandise_action(request)
        elif action == 'change_merchandise':
            return change_merchandise_action(request)
        elif action == 'delete_merchandise':
            return delete_merchandise_action(request)
        else:
            messages.error(request, '未定义的动作，请重试')
            return redirect('AdminFirst:merchandise_management')


def add_merchandise_action(request):
    """ 新增商品动作
    """
    # 获取信息
    name = request.POST.get('name')
    integral_price = request.POST.get('integral_price')
    remain_num = request.POST.get('remain_num')
    description = request.POST.get('description')

    # 新增商品
    Merchandise.objects.create(
        name=name,
        integral_price=integral_price,
        remain_num=remain_num,
        description=description,
    )

    # 记录成功信息
    messages.success(request, '新增成功')
    return redirect('AdminFirst:merchandise_management')


def change_merchandise_action(request):
    """ 修改商品动作
    """
    # 获取信息
    change_id = request.POST.get('change_id')
    change_name = request.POST.get('change_name')
    change_integral_price = request.POST.get('change_integral_price')
    change_remain_num = request.POST.get('change_remain_num')
    change_description = request.POST.get('change_description')

    # 取出要修改的商品
    try:
        merchandise = Merchandise.objects.get(id=change_id)
    except Merchandise.DoesNotExist:
        # 未取到该商品
        messages.error(request, '未取到该商品')
        return redirect('AdminFirst:merchandise_management')
    # 取到该商品了

    # 修改信息
    merchandise.name = change_name
    merchandise.integral_price = change_integral_price
    merchandise.remain_num = change_remain_num
    merchandise.description = change_description
    merchandise.save()

    # 记录成功信息
    messages.success(request, '修改成功')
    return redirect('AdminFirst:merchandise_management')


def delete_merchandise_action(request):
    """ 删除商品
    """
    # 获取要删除的id
    delete_id = request.POST.get('delete_id')

    # 取出要删除的商品
    try:
        merchandise = Merchandise.objects.get(id=delete_id)
    except Merchandise.DoesNotExist:
        # 未取到该商品
        messages.error(request, '未取到该商品')
        return redirect('AdminFirst:merchandise_management')
    # 取到该商品了

    # 标记为删除状态
    merchandise.is_delete = True
    merchandise.save()

    # 记录成功信息
    messages.success(request, '删除成功')
    return redirect('AdminFirst:merchandise_management')

