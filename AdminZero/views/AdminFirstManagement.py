from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from AdminZero.models import AdminZero
from AdminFirst.models import AdminFirst

from utils.GetMD5 import get_md5
from utils.CheckExists import check_job_num_exists


class AdminFirstManagement(View):
    """ 一级管理员管理
    """
    def get(self, request):
        # 登录身份验证
        if request.session.get('who_login') != 'AdminZero':
            request.session.flush()
            return redirect('Login:admin_login')

        # 取出此零级管理员
        admin_zero = AdminZero.objects.get(job_num=request.session.get('job_num'))

        # 获取筛选关键字
        filter_keyword = request.GET.get('filter_keyword', '')
        # 根据筛选关键字筛选一级管理员
        admin_firsts = AdminFirst.objects.filter(
            Q(name__contains=filter_keyword) |
            Q(job_num__contains=filter_keyword)
        )

        # 打包数据
        context = {
            'error_message': request.session.pop('error_message') if request.session.get('error_message') else None,
            'success_message': request.session.pop('success_message') if request.session.get(
                'success_message') else None,
            'filter_keyword': filter_keyword,
            'name': admin_zero.name,
            'admin_firsts': admin_firsts,
        }
        return render(request, 'AdminZero/admin-first-management.html', context=context)

    def post(self, request):
        # 获取动作并判断要执行的操作
        # add 新增
        # change_password 修改密码
        # del 删除
        action = request.POST.get('action')
        if action == 'add':
            # 获取信息
            name = request.POST.get('name')
            job_num = request.POST.get('job_num')
            password = get_md5(request.POST.get('password'))

            # 判断此工号是否已存在
            if check_job_num_exists(job_num):
                # 记录此工号的管理员已存在错误信息
                request.session['error_message'] = '此工号的管理员已存在'
                # 重定向到一级管理员管理页面
                return redirect('AdminZero:admin_first_management')

            # 新增
            AdminFirst.objects.create(
                name=name,
                job_num=job_num,
                password=password
            )
            # 记录成功信息
            request.session['success_message'] = '增加成功'
            # 重定向一级管理员管理页面
            return redirect('AdminZero:admin_first_management')
        elif action == 'change_password':
            # 获取信息
            change_id = request.POST.get('change_id')
            change_password = get_md5(request.POST.get('change_password'))

            # 更改密码
            admin_first = AdminFirst.objects.get(id=change_id)
            admin_first.password = change_password
            admin_first.save()

            # 记录成功信息
            request.session['success_message'] = '密码修改成功'
            # 重定向一级管理员管理页面
            return redirect('AdminZero:admin_first_management')
        elif action == 'del':
            # 获取信息
            del_id = request.POST.get('del_id')

            # 删除
            admin_first = AdminFirst.objects.get(id=del_id)
            admin_first.delete()

            # 记录成功信息
            request.session['success_message'] = '删除成功'
            # 重定向一级管理员管理页面
            return redirect('AdminZero:admin_first_management')
        else:
            # 未知错误，不明的操作
            # 记录非法操作错误并重定向二级管理员管理页面
            request.session['error_message'] = '非法操作类型'
            return redirect('AdminZero:admin_first_management')

