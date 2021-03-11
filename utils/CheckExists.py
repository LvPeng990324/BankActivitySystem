# 与查重操作相关

from AdminThird.models import AdminThird
from AdminSecond.models import AdminSecond
from AdminFirst.models import AdminFirst
from AdminZero.admin import AdminZero
from Customer.models import Customer


def check_job_num_exists(job_num):
    """
    检查给定的工号是否已存在
    :param job_num: 要检查的工号
    :return: 存在：True
             不存在：False
    """
    # 检查现存三级管理员
    if AdminThird.objects.filter(job_num=job_num).exists():
        return True
    # 检查现存二级管理员
    if AdminSecond.objects.filter(job_num=job_num).exists():
        return True
    # 检查现存一级管理员
    if AdminFirst.objects.filter(job_num=job_num).exists():
        return True
    # 检查现存零级管理员
    if AdminZero.objects.filter(job_num=job_num).exists():
        return True

    # 没问题了，返回False
    return False


def check_customer_phone_exists(phone):
    """
    检查给定的客户手机号是否已存在
    :param phone: 要检查的客户手机号
    :return: 存在：True
             不存在：False
    """
    # 检查客户
    if Customer.objects.filter(phone=phone).exists():
        return True

    # 不重复了，返回False
    return False
