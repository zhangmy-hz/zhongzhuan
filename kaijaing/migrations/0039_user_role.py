# Generated by Django 2.1.15 on 2020-07-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0038_auto_20200721_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=20, null=True),
        ),
    ]