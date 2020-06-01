# Generated by Django 3.0.6 on 2020-06-01 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Racelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(unique=True)),
                ('title', models.TextField()),
                ('place', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Racedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horse_name', models.TextField()),
                ('horse_data', models.TextField()),
                ('lackparams', models.TextField()),
                ('racelist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Racelist')),
            ],
        ),
    ]
