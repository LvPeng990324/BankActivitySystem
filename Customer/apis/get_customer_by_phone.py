from django.http import JsonResponse

from Customer.models import Customer


def get_customer_by_phone(request):
    """
    通过手机号获取客户信息
    需要get方法传入客户手机号
    :return: json数据格式
    """
    # 获取客户手机号
    phone = request.GET.get('phone')

    # 取出该客户
    try:
        customer = Customer.objects.get(phone=phone)
    except Customer.DoesNotExist:
        # 未取到该客户，返回未取到标记
        return JsonResponse(data={
            'message': '未找到该客户',
        })

    # 打包响应信息
    response_data = {
        'message': 'ok',
        'customer_id': customer.id,
        'name': customer.name,
    }
    return JsonResponse(data=response_data)
