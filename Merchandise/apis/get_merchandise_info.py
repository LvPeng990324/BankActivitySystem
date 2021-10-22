from django.http import JsonResponse

from Merchandise.models import Merchandise


def get_merchandise_info(request):
    """ 获取商品信息接口
    GET请求
    """
    # 获取要获取信息的商品id
    merchandise_id = request.GET.get('merchandise_id')

    # 取出该商品
    merchandise = Merchandise.objects.get(id=merchandise_id)

    # 打包响应数据
    return JsonResponse(data={
        'name': merchandise.name,
        'remain_num': merchandise.remain_num,
        'integral_price': merchandise.integral_price,
        'description': merchandise.description,
    })



