# 检查客户类型相关自定义tag
from django import template

from Customer.models import Customer

register = template.Library()


@register.filter
def check_customer_merchandise(customer_id):
    """ 检查给定客户是否是商户
    传入客户id，返回布尔值
    """
    # 取出客户
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        # 未取到该客户，返回False
        return False
    # 取到该客户了

    # 返回是否是商户
    return customer.is_merchant is True


