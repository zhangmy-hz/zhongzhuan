# Generated by Django 2.1.15 on 2020-06-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0013_auto_20200616_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wuliu',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
