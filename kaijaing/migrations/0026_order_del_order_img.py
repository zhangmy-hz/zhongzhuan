# Generated by Django 2.1.15 on 2020-06-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0025_auto_20200625_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_del',
            name='order_img',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
