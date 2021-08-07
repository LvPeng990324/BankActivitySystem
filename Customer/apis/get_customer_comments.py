from django.http import JsonResponse

from Customer.models import Customer


def get_customer_comments(request):
    """
    获取客户备注接口
    需要get方法传入客户id
    :return: json数据格式
    """

    # 获取客户id
    customer_id = request.GET.get('customer_id')

    # 获取客户对象
    customer = Customer.objects.get(id=customer_id)

    # 打包相应数据
    response_data = {
        'comment': customer.comment,
    }
    return JsonResponse(response_data)
