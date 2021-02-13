# Generated by Django 3.1.2 on 2021-02-13 01:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_auto_20210213_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 1, 50, 14, 349603, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 1, 50, 14, 348630, tzinfo=utc)),
        ),
    ]
