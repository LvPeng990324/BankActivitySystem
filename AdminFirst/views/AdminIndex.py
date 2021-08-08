from django.db.models import Q
from django.shortcuts import render
from django .views import View
from datetime import datetime
from datetime import timedelta
from django.utils.decorators import method_decorator

from ActivitySignUp.models import ActivityRecord
from ActivitySignUp.models import Activity
from AdminFirst.models import AdminFirst

from utils.login_checker import admin_first_login_required


class AdminIndex(View):
    """ 管理员首页
    """
    @method_decorator(admin_first_login_required)
    def get(self, request):
        # 取出此一级管理员
        admin_first = AdminFirst.objects.get(job_num=request.session.get('job_num'))

        # 客户总数
        total_customer_num = ActivityRecord.objects.all().count()

        # 今日新增客户
        today = datetime.today()
        today_customer_num = ActivityRecord.objects.filter(
            Q(create_time__year=today.year),
            Q(create_time__month=today.month),
            Q(create_time__day=today.day)
        ).count()

        # 取出所有未删除的活动并按创建时间逆序排序
        recent_activities = Activity.objects.filter(is_delete=False).order_by('-create_time')

        # 近期10个活动
        recent_activities_10 = recent_activities[:10]

        # 近期活动客户量
        # 取出最近的7个活动信息
        recent_activities_7 = recent_activities[:7]
        # 记录活动名字并统计此次活动中的客户数量
        recent_activity_customer_num = []  # 记录{'activity_name': 活动名, 'customer_num': 客户数量}关系
        for activity in recent_activities_7:
            # 获取此次活动此二级管理员下所有三级管理员在这个活动中的客户数量以及此活动名字
            customer_num = activity.activityrecord_set.all().count()
            activity_name = activity.name
            # 记录到列表中
            recent_activity_customer_num.append({
                'activity_name': activity_name,
                'customer_num': customer_num,
            })

        # 近两周客户量趋势
        # 获取时间区间
        now_time = datetime.now()
        old_time = now_time - timedelta(weeks=2)
        # 把近两周的客户参与记录取出
        recent_activity_records = ActivityRecord.objects.filter(
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

        # 打包信息
        context = {
            'name': admin_first.name,
            'job_num': request.session.get('job_num'),
            'total_customer_num': total_customer_num,
            'today_customer_num': today_customer_num,
            'recent_activities_10': recent_activities_10,
            'recent_activity_customer_num': recent_activity_customer_num[::-1],  # 为了图表好看，反转元素
            'recent_day_customer_num': recent_day_customer_num[::-1],  # 为了图表好看，反转元素
        }
        return render(request, 'AdminFirst/admin-index.html', context=context)

