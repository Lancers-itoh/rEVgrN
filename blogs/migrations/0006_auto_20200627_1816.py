# Generated by Django 3.0.6 on 2020-06-27 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_racedata_time_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racelist',
            name='racedata_updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 9, 16, 4, 899041, tzinfo=utc)),
        ),
    ]
