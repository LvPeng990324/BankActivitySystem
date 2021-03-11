from django.http import JsonResponse

from .models import NoticeTemplate


def get_notice_template(request):
    # 获取要获取的通知模板id
    notice_template_id = request.GET.get('notice_template_id')
    # 取出通知模板
    notice_template = NoticeTemplate.objects.get(id=notice_template_id)
    # 打包相应数据
    response_data = {
        'title': notice_template.title,
        'content': notice_template.content,
    }
    return JsonResponse(response_data)


