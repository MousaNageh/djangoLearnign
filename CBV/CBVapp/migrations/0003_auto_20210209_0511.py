# Generated by Django 3.1.2 on 2021-02-09 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CBVapp', '0002_auto_20210209_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='CBVapp.school'),
        ),
    ]
