from django.db import models

from AdminSecond.models import AdminSecond


class AdminThird(models.Model):
    """ 三级管理员
    id 唯一标识符
    name 姓名
    job_num 工号
    password 密码
    admin_second 二级管理员 --外键
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    job_num = models.CharField(max_length=20, verbose_name='工号')
    password = models.CharField(max_length=100, verbose_name='密码')
    admin_second = models.ForeignKey(AdminSecond, on_delete=models.SET_NULL, null=True, verbose_name='二级管理员')

    class Meta:
        verbose_name_plural = '三级管理员'
        verbose_name = '三级管理员'

    def __str__(self):
        return self.name
