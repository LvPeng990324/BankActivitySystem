# Generated by Django 3.1.7 on 2021-10-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RequestAction', '0004_auto_20211006_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestactionlog',
            name='finished_time',
            field=models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间'),
        ),
    ]
