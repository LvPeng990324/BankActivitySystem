# Generated by Django 3.1.7 on 2021-10-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Merchandise', '0003_givemerchandiserecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchandise',
            name='integral_price',
            field=models.IntegerField(default=1, help_text='积分价格', verbose_name='积分价格'),
            preserve_default=False,
        ),
    ]