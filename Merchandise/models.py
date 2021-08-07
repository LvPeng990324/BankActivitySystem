from django.db import models


class Merchandise(models.Model):
    """ 商品
    """
    name = models.CharField(max_length=200, verbose_name='商品名', help_text='商品名')
    remain_num = models.IntegerField(verbose_name='库存量', help_text='库存量')
    description = models.TextField(verbose_name='介绍', help_text='介绍')

    class Meta:
        verbose_name_plural = '商品'
        verbose_name = '商品'

    def __str__(self):
        return '{}'.format(self.name)
