from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from datetime import datetime
from datetime import timedelta
from django.utils.decorators import method_decorator

from AdminThird.models import AdminThird
from ActivitySignUp.models import Activity
from ActivitySignUp.models import ActivityRecord

from utils.login_checker import admin_third_login_required


class AdminIndex(View):
    """ 后台管理首页
    """
    @method_decorator(admin_third_login_required)
    def get(self, request):
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

