# Generated by Django 2.1.1 on 2018-09-03 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='valuelog',
            old_name='log_datetime',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='valuelog',
            old_name='device_value',
            new_name='value',
        ),
    ]
