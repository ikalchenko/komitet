# Generated by Django 2.0.6 on 2018-06-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180619_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermissions',
            name='permission',
            field=models.CharField(choices=[('A', 'Admin'), ('RW', 'Read/Write'), ('R', 'Read'), ('B', 'Banned')], max_length=10),
        ),
    ]
