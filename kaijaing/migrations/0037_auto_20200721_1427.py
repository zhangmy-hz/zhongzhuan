# Generated by Django 2.1.15 on 2020-07-21 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0036_roles_del'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roles_del',
            name='code_name',
        ),
        migrations.RemoveField(
            model_name='roles_del',
            name='job_name',
        ),
        migrations.RemoveField(
            model_name='roles_del',
            name='level',
        ),
    ]
