# from django.shortcuts import render
# from django.shortcuts import HttpResponse
# from django.http import JsonResponse
# from django.views import View
#
# from .models import Town
# from .models import Village
# from .models import Group
#
#
# class TownInformation(View):
#     """ 镇子
#     """
#     def get(self, request):
#         pass
#
#
# class VillageInformation(View):
#     """ 村子
#     """
#     def get(self, request):
#         town = request.GET.get('town')
#         villages = list(Village.objects.filter(town__name=town).values('name'))
#         return JsonResponse(villages, safe=False)
#
#
# class GroupInformation(View):
#     """ 组
#     """
#     def get(self, request):
#         village = request.GET.get('village')
#         groups = list(Group.objects.filter(village__name=village).values('name'))
#         return JsonResponse(groups, safe=False)
