from django.db import models

from Customer.models import Customer


class NoticeTemplate(models.Model):
    """ 通知模板
    title 标题
    content 内容
    create_time 创建时间
    """
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '通知模板'
        verbose_name = '通知模板'

    def __str__(self):
        return self.title


class Notice(models.Model):
    """ 通知
    title 标题
    content 内容
    create_time 发布时间
    customer 客户 --外键
    is_read 是否已查看
    """
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    is_read = models.BooleanField(default=False, verbose_name='是否已查看')

    class Meta:
        verbose_name_plural = '通知'
        verbose_name = '通知'

    def __str__(self):
        return self.title
