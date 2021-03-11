from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from AdminThird.models import AdminThird
from AdminSecond.models import AdminSecond
from Customer.models import Customer


class Activity(models.Model):
    """ 活动主体
    id 唯一标识符
    name 活动名
    create_time 发布时间
    describe 介绍
    admin_second 二级管理员
    is_delete 是否已删除
    """
    name = models.CharField(max_length=200, verbose_name='活动名')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    end_time = models.DateTimeField(verbose_name='截止时间')
    content = RichTextUploadingField()
    admin_second = models.ForeignKey(AdminSecond, on_delete=models.SET_NULL, null=True, verbose_name='二级管理员')
    is_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        verbose_name_plural = '活动主体'
        verbose_name = '活动主体'

    def __str__(self):
        return self.name


class ActivityRecord(models.Model):
    """ 活动记录
    id 唯一标识符
    activity 活动 --外键
    customer 客户 --外键
    admin_third 三级管理员 --外键
    create_time 报名时间
    """
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, verbose_name='活动')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='参与客户')
    admin_third = models.ForeignKey(AdminThird, on_delete=models.SET_NULL, null=True, verbose_name='三级管理员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    class Meta:
        verbose_name_plural = '活动记录'
        verbose_name = '活动记录'

    def __str__(self):
        return '{}-{}-{}'.format(
            self.activity.name,
            self.customer.name,
            self.admin_third.name
        )

