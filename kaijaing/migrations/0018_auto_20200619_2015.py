# Generated by Django 2.1.15 on 2020-06-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0017_auto_20200619_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='imageUrl',
            field=models.CharField(max_length=100, null=True),
        ),
    ]