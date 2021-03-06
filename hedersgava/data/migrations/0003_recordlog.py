# Generated by Django 2.1.1 on 2018-09-04 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20180904_0129'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=10)),
                ('device_type', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('log_id', models.IntegerField()),
                ('value', models.FloatField()),
            ],
        ),
    ]
