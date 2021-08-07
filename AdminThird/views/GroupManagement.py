from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import HttpResponseRedirect
from django.views import View

from AdminThird.models import AdminThird
from Address.models import Town
from Address.models import Village
from Address.models import Group


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

