# Generated by Django 2.1.15 on 2020-09-25 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0085_draw_pi_print_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='style_num',
            field=models.FloatField(default=0),
        ),
    ]
