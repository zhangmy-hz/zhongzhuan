# Generated by Django 2.1.15 on 2020-06-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0010_skutype'),
    ]

    operations = [
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=40, null=True)),
                ('unit', models.CharField(max_length=10, null=True)),
                ('barcode', models.CharField(max_length=20, null=True)),
                ('picture', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
