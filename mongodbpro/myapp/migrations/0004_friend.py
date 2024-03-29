# Generated by Django 3.0.5 on 2021-02-18 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210216_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendship_data', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship', to='myapp.User')),
            ],
        ),
    ]
