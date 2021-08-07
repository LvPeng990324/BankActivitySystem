from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect

from Merchandise.models import Merchandise


class MerchandiseManagement(View):
    """ 商品管理
    """
    def get(self, request):
        return render(request, 'AdminSecond/merchandise-management.html')


