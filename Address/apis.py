from django.http import JsonResponse

from .models import Village
from .models import Group


def village_information(request):
    """
    获取镇子下所有村子接口
    需get方法传入镇子名
    :param request:
    :return:
    """
    town = request.GET.get('town')
    villages = list(Village.objects.filter(town__name=town).values('name'))
    return JsonResponse(villages, safe=False)


def group_information(request):
    """
    获取村子下所有组接口
    需get方法传入村子名
    :param request:
    :return:
    """
    village = request.GET.get('village')
    groups = list(Group.objects.filter(village__name=village).values('name'))
    return JsonResponse(groups, safe=False)