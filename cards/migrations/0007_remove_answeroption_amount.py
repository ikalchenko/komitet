# Generated by Django 2.0.6 on 2018-06-21 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_auto_20180620_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answeroption',
            name='amount',
        ),
    ]
