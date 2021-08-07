from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django_redis import get_redis_connection
from datetime import datetime

from Customer.models import Customer
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord
from AdminThird.models import AdminThird
from Address.models import Town
from Address.models import Village
from Address.models import Group


class ActivityForm(View):
    """ 活动报名表类
    """
    def get(self, request):
        # 获取请求参数
        activity_id = request.GET.get('activity_id')
        job_num = request.GET.get('job_num')
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 如果有镇子，则获取所有村名
        villages = []
        if town:
            try:
                villages = Village.objects.filter(town=Town.objects.get(name=town))
            except Town.DoesNotExist:
                # 如果没找到出错了，那就没事儿了，跳过
                pass
        # 如果有村子，则获取所有组名
        groups = []
        if village:
            try:
                groups = Group.objects.filter(village=Village.objects.get(name=village))
            except Village.DoesNotExist:
                # 如果没找到出错了，那就没事儿了，跳过
                pass

        # TODO 验证id是否有效
        # 取出管理员名字
        staff_name = AdminThird.objects.get(job_num=job_num).name
        # 取出活动名
        activity_name = Activity.objects.get(id=activity_id).name
        # 生成图片验证码
        # code_answer, code_img = valid_code()
        # 取出所有镇子
        towns = Town.objects.all()

        # 打包信息返回json
        context = {
            'activity_name': activity_name,
            'staff_name': staff_name,
            'job_num': job_num,
            'activity_id': activity_id,
            # 'code_img': code_img,
            # 'code_answer': code_answer,
            'towns': towns,
            'town': town,
            'village': village,
            'group': group,
            'villages': villages,
            'groups': groups,
        }
        return render(request, 'ActivityManagement/activity-form.html', context=context)

    def post(self, request):
        # 获取提交数据
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        town = request.POST.get('town', '')
        village = request.POST.get('village', '')
        group = request.POST.get('group', '')
        street = request.POST.get('street', '')
        phone = request.POST.get('phone')
        msg_code = request.POST.get('msg_code')
        activity_id = request.POST.get('activity_id')
        job_num = request.POST.get('job_num')

        # 验证短信验证码
        # 从redis取出此手机号的短信验证码
        redis_cli = get_redis_connection('msg_code')
        correct_msg_code = redis_cli.get(phone)  # 取出来是b数据，需要解码
        # 如果redis中有记录才进行解码操作，避免对None进行decode而报错
        if correct_msg_code:
            correct_msg_code = correct_msg_code.decode()
        # 比对
        # 如果不对就记录短信验证码有误错误并重新加载该报名页面
        if correct_msg_code != msg_code:
            context = {
                'activity_name': Activity.objects.get(id=activity_id).name,
                'staff_name': AdminThird.objects.get(job_num=job_num).name,
                'error_message': '短信验证码有误！',
            }
            return render(request, 'ActivityManagement/activity-form.html', context=context)

        # 判断是否是老客户
        customer = Customer.objects.filter(phone=phone)
        if customer.exists():
            # 老客户
            # 记录是老客户
            customer_exists = True
            # 取出客户信息
            customer = customer[0]
        else:
            # 新客户
            # 记录是新客户
            customer_exists = False
            # 增加客户信息
            customer = Customer.objects.create(
                name=name,
                gender=gender,
                phone=phone,
                town=town,
                village=village,
                group=group,
                street=street,
            )

        # 如果是老客户，判断是否已报名过此活动
        if customer_exists:
            # 从活动记录中查询此活动此客户信息
            # 存在就返回已报名的错误信息
            if ActivityRecord.objects.filter(activity_id=activity_id, customer_id=customer.id):
                # 清除session记录并记录此客户的登录信息
                request.session.flush()
                request.session['who_login'] = 'Customer'
                request.session['customer_phone'] = phone
                # 显示跳转页面
                context = {
                    'message': '您已参加此活动',
                }
                return render(request, 'ActivityManagement/wait-to-customer-index.html', context=context)

        # 判断此活动是否已删除/截止
        # 取出该活动
        activity = Activity.objects.get(id=activity_id)
        # 取出截止时间以及是否已删除标记
        end_time = activity.end_time
        is_delete = activity.is_delete
        # 进行已删除/已截止判断
        if is_delete or end_time < datetime.now():
            return HttpResponse('<h1>此活动已截止或已经被删除，您现在无法报名</h1>')

        # 记录报名记录
        ActivityRecord.objects.create(
            activity=activity,
            customer=customer,
            admin_third=AdminThird.objects.get(job_num=job_num),
        )

        # 清除session记录并记录此客户的登录信息
        request.session.flush()
        request.session['who_login'] = 'Customer'
        request.session['customer_phone'] = phone

        # 提示成功
        context = {
            'message': '报名成功',
        }
        return render(request, 'ActivityManagement/wait-to-customer-index.html', context=context)

