# Generated by Django 2.1.15 on 2020-06-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaijaing', '0020_auto_20200619_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Del',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=20)),
                ('item_code', models.CharField(max_length=20)),
                ('item_name', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=10)),
                ('skutype', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('words', models.CharField(max_length=30)),
                ('num', models.IntegerField(max_length=10)),
                ('total_num', models.IntegerField(max_length=10)),
                ('wuliu', models.CharField(max_length=30)),
                ('lianchang', models.IntegerField(max_length=20)),
                ('note', models.CharField(max_length=200, null=True)),
                ('size', models.FloatField(max_length=20)),
                ('create_date', models.CharField(max_length=20, null=True)),
                ('end_date', models.CharField(max_length=20, null=True)),
                ('state', models.CharField(default='未审核', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='create_user',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
