# Generated by Django 2.1.15 on 2020-08-13 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0053_order_del_print_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_del',
            name='ruku_status',
        ),
    ]