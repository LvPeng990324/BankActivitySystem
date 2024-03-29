# Generated by Django 3.1.7 on 2021-10-06 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0009_customer_is_catering_merchant'),
        ('RequestAction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestaction',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='requestaction',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='requestaction',
            name='is_finished',
        ),
        migrations.RemoveField(
            model_name='requestaction',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='requestaction',
            name='start_date',
        ),
        migrations.CreateModel(
            name='RequestActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=128, verbose_name='名称')),
                ('remark', models.TextField(help_text='备注', verbose_name='备注')),
                ('start_date', models.DateField(blank=True, help_text='起始日期', null=True, verbose_name='起始日期')),
                ('end_date', models.DateField(blank=True, help_text='截止日期', null=True, verbose_name='截止日期')),
                ('is_finished', models.BooleanField(default=False, help_text='是否已完成', verbose_name='是否已完成')),
                ('customer', models.ForeignKey(help_text='客户', on_delete=django.db.models.deletion.CASCADE, to='Customer.customer', verbose_name='客户')),
            ],
            options={
                'verbose_name': '请求记录',
                'verbose_name_plural': '请求记录',
            },
        ),
    ]
