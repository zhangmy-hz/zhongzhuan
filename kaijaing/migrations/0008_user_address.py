# Generated by Django 2.1.15 on 2020-06-13 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0007_auto_20200611_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=20, null=True),
        ),
    ]