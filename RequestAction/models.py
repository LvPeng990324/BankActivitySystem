from django.db import models

from Customer.models import Customer


class RequestAction(models.Model):
    """ 请求动作
    在商户类型的客户的商户特权页面可以看到并选择动作来进行请求
    动作类型可以由相应的管理员进行管理
    上级用户也可以代理用户发出动作，并规定完成时间段
    """
    name = models.CharField(max_length=128, verbose_name='名称', help_text='名称')

    class Meta:
        verbose_name_plural = '请求动作'
        verbose_name = '请求动作'

    def __str__(self):
        return '{}-{}'.format(
            self.id,
            self.name,
        )


class RequestActionLog(models.Model):
    """ 请求记录
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户', help_text='客户')

    name = models.CharField(max_length=128, verbose_name='名称', help_text='名称')
    remark = models.TextField(null=True, blank=True, verbose_name='备注', help_text='备注')
    start_date = models.DateField(null=True, blank=True, verbose_name='起始日期', help_text='起始日期')
    end_date = models.DateField(null=True, blank=True, verbose_name='截止日期', help_text='截止日期')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')

    is_finished = models.BooleanField(default=False, verbose_name='是否已完成', help_text='是否已完成')

    class Meta:
        verbose_name_plural = '请求记录'
        verbose_name = '请求记录'

    def __str__(self):
        return '{}-{}-{}'.format(
            self.customer.name,
            self.name,
            self.is_finished,
        )

