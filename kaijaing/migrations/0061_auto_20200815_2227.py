# Generated by Django 2.1.15 on 2020-08-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0060_auto_20200815_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehous_del',
            name='color',
        ),
        migrations.RemoveField(
            model_name='warehous_del',
            name='total_num',
        ),
        migrations.AddField(
            model_name='warehous_del',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='warehous_del',
            name='supplier',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='warehous_del',
            name='total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='warehousing',
            name='supplier',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='warehous_del',
            name='num',
            field=models.IntegerField(),
        ),
    ]
