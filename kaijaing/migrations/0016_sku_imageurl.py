# Generated by Django 2.1.15 on 2020-06-18 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0015_wenzi'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='imageUrl',
            field=models.BooleanField(max_length=20, null=True),
        ),
    ]