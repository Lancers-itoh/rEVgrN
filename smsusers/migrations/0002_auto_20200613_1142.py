# Generated by Django 3.0.6 on 2020-06-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsusers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ademail',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
