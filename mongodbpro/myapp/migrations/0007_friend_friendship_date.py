# Generated by Django 3.0.5 on 2021-02-18 04:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210218_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='friendship_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 4, 18, 52, 875462, tzinfo=utc)),
        ),
    ]
