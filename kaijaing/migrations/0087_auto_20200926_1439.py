# Generated by Django 2.1.15 on 2020-09-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0086_sku_style_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_del',
            name='draw_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order_del',
            name='draw_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order_del',
            name='style_num',
            field=models.FloatField(default=0),
        ),
    ]
