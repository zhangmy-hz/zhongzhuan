# Generated by Django 2.1.15 on 2020-07-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0031_order_del_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_del',
            name='draw_img',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
