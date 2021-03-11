from django.db import models


class AdminZero(models.Model):
    """ 零级管理员
    name 姓名
    job_num 工号
    password 密码
    """
    name = models.CharField(max_length=20, verbose_name='姓名')
    job_num = models.CharField(max_length=20, verbose_name='工号')
    password = models.CharField(max_length=100, verbose_name='密码')

    class Meta:
        verbose_name_plural = '零级管理员'
        verbose_name = '零级管理员'

    def __str__(self):
        return self.name
