from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from ActivitySignUp.models import Activity


class ActivityInformation(View):
    """ 活动信息类
    """
    def get(self, request):
        # 获取要查询的活动id以及管理员工号
        activity_id = request.GET.get('activity_id')
        job_num = request.GET.get('job_num')
        # 获取可能有的地址信息
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')

        # 查询活动信息
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            # 不存在，返回不存在错误信息
            return HttpResponse('<h1>活动不存在</h1>')

        # 打包数据引导活动介绍页面
        context = {
            'activity_name': activity.name,
            'content': activity.content,
            'job_num': job_num,
            'activity_id': activity_id,
            'town': town,
            'village': village,
            'group': group,
        }
        return render(request, 'ActivityManagement/activity-information.html', context=context)

