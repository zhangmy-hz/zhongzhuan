# Generated by Django 2.1.15 on 2020-06-16 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0012_sku_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='create_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='people',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
