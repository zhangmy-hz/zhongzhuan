# Generated by Django 2.1.15 on 2020-07-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0035_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles_Del',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=40)),
                ('code_name', models.CharField(max_length=20)),
                ('jon_code', models.CharField(max_length=20)),
                ('job_name', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=2, null=True)),
            ],
        ),
    ]