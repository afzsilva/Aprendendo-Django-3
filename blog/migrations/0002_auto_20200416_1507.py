# Generated by Django 3.0.5 on 2020-04-16 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2020, 4, 16, 15, 7, 3, 941093, tzinfo=utc)),
        ),
    ]
