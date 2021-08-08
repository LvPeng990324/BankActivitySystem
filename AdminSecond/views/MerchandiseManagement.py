from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from Merchandise.models import Merchandise

from utils.login_checker import admin_second_login_required


class MerchandiseManagement(View):
    """ 商品管理
    """
    @method_decorator(admin_second_login_required)
    def get(self, request):

        return render(request, 'AdminSecond/merchandise-management.html')


