# Generated by Django 2.1.15 on 2020-08-11 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0048_roles_del_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw_Pi',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('create_time', models.CharField(max_length=40, null=True)),
                ('create_user', models.CharField(max_length=40, null=True)),
            ],
        ),
    ]
