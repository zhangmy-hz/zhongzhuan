# Generated by Django 2.1.15 on 2020-06-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0005_auto_20200610_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nameid',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
