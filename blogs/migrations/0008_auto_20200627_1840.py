# Generated by Django 3.0.6 on 2020-06-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20200627_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racelist',
            name='racedata_updated_at',
            field=models.DateTimeField(),
        ),
    ]
