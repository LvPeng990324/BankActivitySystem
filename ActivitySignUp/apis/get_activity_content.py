from django.http import JsonResponse

from ActivitySignUp.models import Activity


def get_activity_content(request):
    """
    获取活动介绍方法
    需get方法传入活动id
    :param request:
    :return: 指定活动的介绍
    """
    # 获取要获取介绍的活动id
    activity_id = request.GET.get('activity_id')

    # 取出此活动
    activity = Activity.objects.get(id=activity_id)
    # 取出介绍
    content = activity.content

    # 打包相应数据
    response_data = {
        'content': content,
    }
    return JsonResponse(response_data)