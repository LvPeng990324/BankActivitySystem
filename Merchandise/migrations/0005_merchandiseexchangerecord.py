# Generated by Django 3.1.7 on 2021-10-21 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0010_customer_integral'),
        ('Merchandise', '0004_merchandise_integral_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchandiseExchangeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('is_exchanged', models.BooleanField(default=False, help_text='是否已兑换', verbose_name='是否已兑换')),
                ('exchanged_time', models.DateTimeField(blank=True, help_text='完成兑换时间', null=True, verbose_name='完成兑换时间')),
                ('customer', models.ForeignKey(help_text='客户', on_delete=django.db.models.deletion.CASCADE, to='Customer.customer', verbose_name='客户')),
                ('merchandise', models.ForeignKey(help_text='商品', on_delete=django.db.models.deletion.CASCADE, to='Merchandise.merchandise', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品兑换记录',
                'verbose_name_plural': '商品兑换记录',
            },
        ),
    ]