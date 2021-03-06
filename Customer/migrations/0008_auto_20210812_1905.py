# Generated by Django 3.1.7 on 2021-08-12 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0007_customer_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_installed_micro_post_pay',
            field=models.BooleanField(blank=True, help_text='是否安装微邮付', null=True, verbose_name='是否安装微邮付'),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_merchant',
            field=models.BooleanField(blank=True, help_text='是否为商户', null=True, verbose_name='是否为商户'),
        ),
        migrations.AddField(
            model_name='customer',
            name='salt_delivery',
            field=models.CharField(blank=True, help_text='食盐配送', max_length=100, null=True, verbose_name='食盐配送'),
        ),
    ]
