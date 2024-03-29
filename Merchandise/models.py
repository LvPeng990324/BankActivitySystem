from django.db import models

from Customer.models import Customer


class Merchandise(models.Model):
    """ 商品
    """
    name = models.CharField(max_length=200, verbose_name='商品名', help_text='商品名')
    remain_num = models.IntegerField(verbose_name='库存量', help_text='库存量')
    integral_price = models.IntegerField(verbose_name='积分价格', help_text='积分价格')
    description = models.TextField(verbose_name='介绍', help_text='介绍')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除', help_text='是否删除')

    class Meta:
        verbose_name_plural = '商品'
        verbose_name = '商品'

    def __str__(self):
        return '{}'.format(self.name)


class MerchandiseExchangeRecord(models.Model):
    """ 商品兑换记录
    """
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE, verbose_name='商品', help_text='商品')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户', help_text='客户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    is_exchanged = models.BooleanField(default=False, verbose_name='是否已兑换', help_text='是否已兑换')
    exchanged_time = models.DateTimeField(null=True, blank=True, verbose_name='完成兑换时间', help_text='完成兑换时间')

    class Meta:
        verbose_name_plural = '商品兑换记录'
        verbose_name = '商品兑换记录'

    def __str__(self):
        return '{}-{}-{}-{}'.format(
            self.id,
            self.merchandise.name,
            self.customer.name,
            self.is_exchanged,
        )


class GiveMerchandiseRecord(models.Model):
    """ 商品发放记录
    """
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE, verbose_name='商品', help_text='商品')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户', help_text='客户')
    give_num = models.IntegerField(verbose_name='发放数量', help_text='发放数量')
    give_time = models.DateTimeField(auto_now_add=True, verbose_name='发放时间', help_text='发放时间')
    give_admin_name = models.CharField(max_length=200, verbose_name='管理员姓名', help_text='管理员姓名')

    class Meta:
        verbose_name_plural = '商品发放记录'
        verbose_name = '商品发放记录'

    def __str__(self):
        return '{}-{}-{}'.format(
            self.merchandise.name,
            self.customer.name,
            self.give_num,
        )
