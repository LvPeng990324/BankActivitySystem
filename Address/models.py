from django.db import models


class Town(models.Model):
    """ 镇子
    """
    name = models.CharField(max_length=20, verbose_name='镇名')

    class Meta:
        verbose_name_plural = '镇子'
        verbose_name = '镇子'

    def __str__(self):
        return self.name


class Village(models.Model):
    """ 村子
    """
    name = models.CharField(max_length=20, verbose_name='村名')
    town = models.ForeignKey(Town, on_delete=models.CASCADE, verbose_name='镇名')

    class Meta:
        verbose_name_plural = '村子'
        verbose_name = '村子'

    def __str__(self):
        return self.name


class Group(models.Model):
    """ 组
    """
    name = models.CharField(max_length=20, verbose_name='组名')
    village = models.ForeignKey(Village, on_delete=models.CASCADE, verbose_name='村名')

    class Meta:
        verbose_name_plural = '组'
        verbose_name = '组'

    def __str__(self):
        return self.name
