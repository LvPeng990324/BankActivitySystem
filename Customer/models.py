from django.db import models


class Customer(models.Model):
    """ 客户
    id 唯一标识符
    name 姓名
    gender 性别
    town 镇子
    village 村子
    group 组
    street 街道
    phone 手机号码
    tag 标签
    tag_type 标签类型
    is_vip 是否会员
    card_num 邮政卡卡号
    comment 备注
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.CharField(max_length=4, verbose_name='性别')
    town = models.CharField(max_length=20, default='', verbose_name='镇子')
    village = models.CharField(max_length=20, default='', verbose_name='村子')
    group = models.CharField(max_length=20, default='', verbose_name='组')
    street = models.CharField(max_length=20, default='', verbose_name='街道')
    phone = models.CharField(max_length=20, verbose_name='手机号码')
    tag = models.CharField(max_length=100, default='无', verbose_name='标签')
    tag_type = models.CharField(max_length=20, default='secondary', verbose_name='标签类型')
    is_vip = models.BooleanField(default=False, verbose_name='是否会员')
    card_num = models.CharField(max_length=20, default='', verbose_name='邮政卡卡号')
    password = models.CharField(max_length=100, default='', verbose_name='密码')
    comment = models.TextField(default='', verbose_name='备注')

    class Meta:
        verbose_name_plural = '客户'
        verbose_name = '客户'

    def __str__(self):
        return self.name


