from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import HttpResponseRedirect
from django.views import View
from datetime import datetime
from datetime import timedelta
from BankActivitySystem.settings import DEPLOY_DOMAIN

from .models import AdminThird
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord
from Customer.models import Customer
from Notice.models import NoticeTemplate
from Address.models import Town
from Address.models import Village
from Address.models import Group

from utils.GetMD5 import get_md5
from utils.QRCode import get_qrcode_stream
from utils.SendNotice import send_one
from utils.SendNotice import batch_send
from utils.CheckExists import check_customer_phone_exists


class AdminIndex(View):
    """ 后台管理首页
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取页面信息
        admin = AdminThird.objects.get(job_num=request.session.get('job_num'))
        # 客户总数
        total_customer_num = admin.activityrecord_set.count()
        # 今日新增客户
        today_customer_num = admin.activityrecord_set.filter(
            Q(create_time__year=datetime.today().year),
            Q(create_time__month=datetime.today().month),
            Q(create_time__day=datetime.today().day),
        ).count()

        # 取出所有未删除的活动并按时间逆序排序
        recent_activities = Activity.objects.filter(is_delete=False).order_by('-create_time')

        # 近期活动我的客户量
        # 取出最近的7个活动信息
        recent_activities_7 = recent_activities[:7]
        # 记录活动名字并分别统计此三级管理员的客户量
        recent_activity_my_customer_num = []  # 记录{'activity_name': 活动名, 'customer_num': 客户数量}关系
        for activity in recent_activities_7:
            # 获取此次活动此三级管理员的客户数量以及此活动名字
            customer_num = activity.activityrecord_set.filter(admin_third=admin).count()
            activity_name = activity.name
            # 记录到列表中
            recent_activity_my_customer_num.append({
                'activity_name': activity_name,
                'customer_num': customer_num,
            })

        # 两周我的客户量趋势
        # 获取时间区间
        now_time = datetime.now()
        old_time = now_time - timedelta(weeks=2)
        # 把近两周此三级管理员获得的客户参与记录取出
        recent_activity_records = ActivityRecord.objects.filter(
            Q(admin_third=admin),
            Q(create_time__gte=old_time),
            Q(create_time__lte=now_time),
        )
        # 获取时间区间内每一天的时间对象
        # 查询每天的客户量并记录到{'time': 时间, 'customer_num': 客户数量}关系中
        recent_day_customer_num = []
        for temp_day in range(15):
            # 获取这一天时间对象
            temp_old_time = now_time - timedelta(days=temp_day)
            # 查询这一天的客户数量
            customer_num = recent_activity_records.filter(
                Q(create_time__year=temp_old_time.year),
                Q(create_time__month=temp_old_time.month),
                Q(create_time__day=temp_old_time.day),
            ).count()
            # 记录到列表中
            recent_day_customer_num.append({
                'time': temp_old_time,
                'customer_num': customer_num,
            })

        # 近期活动，选取最新的10条活动
        recent_activities_10 = recent_activities[:10]

        context = {
            'job_num': request.session.get('job_num'),
            'name': admin.name,
            'total_customer_num': total_customer_num,
            'today_customer_num': today_customer_num,
            'recent_activity_my_customer_num': recent_activity_my_customer_num[::-1],  # 为了图表好看，把列表元素逆序
            'recent_activities_10': recent_activities_10,
            'recent_day_customer_num': recent_day_customer_num[::-1],  # 为了图表好看，把列表元素逆序
        }
        return render(request, 'AdminThird/admin-index.html', context=context)


class Profile(View):
    """ 个人信息
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出个人信息
        job_num = request.session.get('job_num')
        name = AdminThird.objects.get(job_num=job_num)

        # 打包信息
        context = {
            'job_num': job_num,
            'name': name,
        }
        return render(request, 'AdminThird/profile.html', context=context)

    def post(self, request):
        # 暂时没有什么可以改的
        pass


class ChangePassword(View):
    """ 修改密码
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 打包可能存在的错误/成功信息
        context = {
            'name': AdminThird.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get('success_message') else None,
        }
        return render(request, 'AdminThird/change-password.html', context=context)

    def post(self, request):
        # 从前端取得填写的旧密码以及两次新密码
        old_password = get_md5((request.POST.get('old_password')))
        new_password = get_md5((request.POST.get('new_password')))
        confirm_password = get_md5((request.POST.get('confirm_password')))

        # 对比旧密码是否正确
        admin = AdminThird.objects.get(job_num=request.session.get('job_num'))
        current_password = admin.password
        if old_password != current_password:
            # 旧密码错误
            request.session['error_message'] = '旧密码有误！'
            return redirect('AdminThird:change_password')
        # 对比两次确认密码是否一致
        if new_password != confirm_password:
            # 不一致错误
            request.session['error_message'] = '两次新密码不一致！'
            return redirect('AdminThird:change_password')

        # 更新密码
        admin.password = new_password
        admin.save()

        # 记录成功信息
        request.session['success_message'] = '密码修改成功'
        # 重定向密码更改页面
        return redirect('AdminThird:change_password')


class CustomerManagement(View):
    """ 客户管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取一开始要筛选的镇子、村子、组
        town = request.GET.get('town', '')
        village = request.GET.get('village', '')
        group = request.GET.get('group', '')
        # 判断是否有镇子，如果没有，则表示是第一次进入，还没选择地址范围
        # 引导客户管理-地址选择页面
        if not town:
            # 打包数据
            context = {
                'name': admin_third.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminThird/customer-management-select-address.html', context=context)

        # 如果是所有镇子，就重置为空字符串来实现筛选所有
        if town == '所有镇子':
            town = ''
        # 获取可能的筛选字段并筛选活动记录
        # 并且同时根据地址范围筛选
        filter_keyword = request.GET.get('filter_keyword', '')
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third=AdminThird.objects.get(job_num=request.session.get('job_num'))),
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword),
            Q(customer__town__contains=town),
            Q(customer__village__contains=village),
            Q(customer__group__contains=group)
        )

        # 获取所有通知模板，按发布时间逆序排序
        notice_templates = NoticeTemplate.objects.all().order_by('-create_time')

        # 打包可能存在的错误/成功信息
        # 未截止的活动，按创建时间倒序
        # 与当前三级管理员有关的活动参与记录，按报名时间倒序
        context = {
            'filter_keyword': filter_keyword,
            'activities': Activity.objects.filter(end_time__gte=datetime.now()).order_by('-create_time'),
            'activity_records': activity_records.order_by('-create_time'),
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'notice_templates': notice_templates,
            'town': town,
            'village': village,
            'group': group,
            'towns': Town.objects.all(),
        }
        return render(request, 'AdminThird/customer-management.html', context=context)

    def post(self, request):
        # 获取一开始的区域筛选信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')

        # 获取前端的动作
        # add 增加
        # change 修改
        # del 删除
        # change_tag 修改标签
        # send_notice 发送通知
        # change_comment 修改备注
        action = request.POST.get('action')
        if action == 'add':
            # 获取填写的用户信息
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            town_add = request.POST.get('town_add')
            village_add = request.POST.get('village_add')
            group_add = request.POST.get('group_add')
            street_add = request.POST.get('street_add')
            activity_id = request.POST.get('activity')

            # 判断此手机号是否已在客户数据库中
            # 没有就创建，有就直接取出
            if check_customer_phone_exists(phone):
                # 存在，直接取出
                customer = Customer.objects.get(phone=phone)
            else:
                # 不存在，创建
                customer = Customer.objects.create(
                    name=name,
                    gender=gender,
                    town=town_add,
                    village=village_add,
                    group=group_add,
                    street=street_add,
                    phone=phone,
                )

            # 判断此客户是否已经参加了此活动
            if ActivityRecord.objects.filter(activity_id=activity_id, customer_id=customer.id):
                # 已参加了此活动，记录客户已参加此活动错误
                request.session['error_message'] = '该客户已参加此活动！'
                # 重定向客户管理页面
                return redirect('AdminThird:customer_management')

            # 没问题了，创建记录
            ActivityRecord.objects.create(
                activity=Activity.objects.get(id=activity_id),
                customer=customer,
                admin_third=AdminThird.objects.get(job_num=request.session.get('job_num')),
            )
            # 记录成功信息并重定向客户管理页面
            request.session['success_message'] = '增加成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change':
            # 从前端获取要修改的信息
            change_id = request.POST.get('change_id')
            change_name = request.POST.get('change_name')
            change_gender = request.POST.get('change_gender')
            change_phone = request.POST.get('change_phone')
            change_town = request.POST.get('change_town')
            change_village = request.POST.get('change_village')
            change_group = request.POST.get('change_group')
            change_street = request.POST.get('change_street')

            # 取出该客户信息并进行修改
            customer = Customer.objects.get(id=change_id)
            customer.name = change_name
            customer.gender = change_gender
            customer.phone = change_phone
            customer.town = change_town
            customer.village = change_village
            customer.group = change_group
            customer.street = change_street
            customer.save()

            # 记录修改成功提示并重定向客户管理页面
            request.session['success_message'] = '信息修改成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'del':
            # 从前端获取要删除的记录id
            del_id = request.POST.get('del_id')

            # 从活动记录表中取出该条记录并删除
            activity_record = ActivityRecord.objects.get(id=del_id)
            activity_record.delete()

            # 记录删除成功信息并重定向客户管理页面
            request.session['success_message'] = '记录删除成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_tag':
            change_id = request.POST.get('change_id')
            change_tag = request.POST.get('change_tag')
            change_tag_type = request.POST.get('change_tag_type')
            # 取出客户并更改信息
            customer = Customer.objects.get(id=change_id)
            customer.tag = change_tag
            customer.tag_type = change_tag_type
            customer.save()
            # 记录成功信息并重定向客户管理页面
            request.session['success_message'] = '修改成功'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'send_notice':
            # 获取信息
            send_customer_id = request.POST.get('send_customer_id')
            notice_template_id = request.POST.get('notice_id')
            need_msg = request.POST.get('need_msg')

            # 推送通知
            send_one(send_customer_id, notice_template_id, need_msg)

            # 记录成功信息
            request.session['success_message'] = '通知发送成功'
            # 重定向客户管理页面
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        elif action == 'change_comment':
            # 获取信息
            comment_customer_id = request.POST.get('comment_customer_id')
            customer_comment = request.POST.get('customer_comment')

            # 获取此客户
            customer = Customer.objects.get(id=comment_customer_id)
            # 修改备注信息
            customer.comment = customer_comment
            customer.save()

            # 记录成功信息
            request.session['success_message'] = '备注修改成功'
            # 重定向客户管理页面
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向客户管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect(
                reverse('AdminThird:customer_management') + '?town={}&village={}&group={}'.format(town, village, group)
            )


class NoticeView(View):
    """ 通知查看
    """
    def get(self, request):
        # 验证登录身份
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键字筛选通知模板，并根据创建时间逆序排序
        notice_templates = NoticeTemplate.objects.filter(
            Q(title__contains=filter_keyword)
        ).order_by('-create_time')

        # 打包数据
        context = {
            'filter_keyword': filter_keyword,
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminThird/notice-view.html', context=context)


class GenerateQRCode(View):
    """ 活动二维码
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取可能有的筛选字段并筛选活动信息
        filter_keyword = request.GET.get('filter_keyword', '')
        activities = Activity.objects.filter(
            Q(name__contains=filter_keyword),
        )

        # 获取所有镇子信息
        towns = Town.objects.all()

        # 打包信息
        context = {
            'name': AdminThird.objects.get(job_num=request.session.get('job_num')).name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'activities': activities,
            'towns': towns,
        }
        return render(request, 'AdminThird/generate-qrcode.html', context=context)

    def post(self, request):
        # 获取要生成二维码的活动id
        activity_id = request.POST.get('activity_id')

        # 判断此活动是否已截止
        end_time = Activity.objects.get(id=activity_id).end_time
        now_time = datetime.now()
        if end_time < now_time:
            return HttpResponse('<h1>此活动已截止，不可报名</h1>')

        # 记录此三级管理员工号
        job_num = request.session.get('job_num')
        # 获取可能选择的地址信息
        town = request.POST.get('town')
        village = request.POST.get('village')
        group = request.POST.get('group')
        # 组合生成二维码需要的URL
        # 127.0.0.1:8000/activity-sign-up/activity-information/?job_num=0001&activity_id=3&town=城关镇&village=北关社区&group=1组
        qrcode_url = '{domain}/activity-sign-up/activity-information/?job_num={job_num}&activity_id={activity_id}&town={town}&village={village}&group={group}'.format(
            domain=DEPLOY_DOMAIN,
            job_num=job_num,
            activity_id=activity_id,
            town=town,
            village=village,
            group=group,
        )
        # 生成IO流的二维码数据
        qrcode_stream = get_qrcode_stream(qrcode_url)
        # 显示二维码
        return HttpResponse(qrcode_stream, content_type='image/png')


class GroupManagement(View):
    """ 组管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 获取此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 尝试获取村名
        village_name = request.GET.get('village', None)
        # 如果没有村名，则表示是第一次访问，还未选择村名
        # 引导组管理-选择村名页面
        if not village_name:
            context = {
                'name': admin_third.name,
                'towns': Town.objects.all(),
            }
            return render(request, 'AdminThird/group-management-select-village.html', context=context)

        # 获取到了村名，表示是选择好了要管理的村子
        # 取出此村子下所有的组信息
        village = Village.objects.get(name=village_name)
        groups = Group.objects.filter(village=village)

        # 打包数据
        context = {
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'village_name': village_name,
            'groups': groups,
        }
        return render(request, 'AdminThird/group-management.html', context=context)

    def post(self, request):
        # 获取动作
        action = request.POST.get('action')
        # 判断要执行的动作
        # add 新增
        # del 删除
        if action == 'add':
            # 获取要增加的组名
            group_name = request.POST.get('group_name')
            # 获取村名
            village_name = request.POST.get('village_name')

            # 新增组
            Group.objects.create(
                name=group_name,
                village=Village.objects.get(name=village_name)
            )

            # 记录成功信息
            request.session['success_message'] = '新增成功'
            # 重定向此村下组管理页面
            return HttpResponseRedirect(reverse('AdminThird:group_management') + '?village={}'.format(village_name))
        elif action == 'del':
            # 获取要删除的组的id
            del_id = request.POST.get('del_id')
            # 删除
            del_group = Group.objects.get(id=del_id)
            del_group.delete()

            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向此村下组管理页面
            village_name = request.POST.get('village_name')
            return HttpResponseRedirect(reverse('AdminThird:group_management') + '?village={}'.format(village_name))
        else:
            # 未知动作
            # 记录未知操作错误信息，并重定向组管理页面
            request.session['error_message'] = '未知的操作'
            return redirect('AdminThird:group_management')


class BatchSend(View):
    """ 批量推送
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminThird':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此三级管理员
        admin_third = AdminThird.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键词
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据关键词筛选客户参与记录
        activity_records = ActivityRecord.objects.filter(
            Q(admin_third=AdminThird.objects.get(job_num=request.session.get('job_num'))),
            Q(customer__name__contains=filter_keyword) |
            Q(customer__gender__contains=filter_keyword) |
            Q(customer__phone__contains=filter_keyword) |
            Q(customer__town__contains=filter_keyword) |
            Q(customer__village__contains=filter_keyword) |
            Q(customer__group__contains=filter_keyword) |
            Q(customer__street__contains=filter_keyword) |
            Q(customer__tag__contains=filter_keyword) |
            Q(activity__name__contains=filter_keyword)
        )

        # 获取所有通知模板，按发布时间逆序排序
        notice_templates = NoticeTemplate.objects.all().order_by('-create_time')

        # 打包数据
        context = {
            'name': admin_third.name,
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'activity_records': activity_records,
            'notice_templates': notice_templates,
        }
        return render(request, 'AdminThird/batch-send.html', context=context)

    def post(self, request):
        # 获取信息
        send_customer_ids = request.POST.get('send_customer_ids')
        notice_id = request.POST.get('notice_id')
        need_msg = request.POST.get('need_msg')

        # 推送通知
        batch_send(send_customer_ids, notice_id, need_msg)

        # 记录成功信息
        request.session['success_message'] = '通知推送成功'
        # 重定向批量推送页面
        return redirect('AdminThird:batch_send')


