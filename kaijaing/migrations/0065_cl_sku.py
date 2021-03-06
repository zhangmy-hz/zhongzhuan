# Generated by Django 2.1.15 on 2020-08-16 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0064_contacts_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='cl_SKU',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('format', models.CharField(max_length=20, null=True)),
                ('unit', models.CharField(max_length=20, null=True)),
                ('note', models.CharField(max_length=220, null=True)),
                ('create_date', models.CharField(max_length=20, null=True)),
                ('create_user', models.CharField(max_length=20, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
