# Generated by Django 3.0.6 on 2020-06-27 09:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_auto_20200627_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='racelist',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='racelist',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='racelist',
            name='racedata_updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 9, 19, 15, 887524, tzinfo=utc)),
        ),
    ]
