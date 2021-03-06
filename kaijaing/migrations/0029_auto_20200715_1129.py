# Generated by Django 2.1.15 on 2020-07-15 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0028_order_del_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_del',
            name='chuku_status',
            field=models.CharField(default='未出库', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order_del',
            name='draw_status',
            field=models.CharField(default='未画图', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order_del',
            name='page_status',
            field=models.CharField(default='未包装', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order_del',
            name='ruku_status',
            field=models.CharField(default='未入库', max_length=10, null=True),
        ),
    ]
