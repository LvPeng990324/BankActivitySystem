# Generated by Django 3.1.5 on 2021-02-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0005_auto_20210224_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.AddField(
            model_name='customer',
            name='street',
            field=models.CharField(default='', max_length=20, verbose_name='街道'),
        ),
    ]
