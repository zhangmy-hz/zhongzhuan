# Generated by Django 2.1.15 on 2020-09-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0080_order_pi_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='draw_pi',
            name='note',
            field=models.CharField(max_length=200, null=True),
        ),
    ]