# Generated by Django 2.1.15 on 2020-08-11 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0049_draw_pi'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_del',
            name='pi_code',
            field=models.CharField(default='', max_length=30),
        ),
    ]