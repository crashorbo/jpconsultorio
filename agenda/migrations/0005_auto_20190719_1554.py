# Generated by Django 2.1.4 on 2019-07-19 19:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_auto_20190708_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='codigo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 7, 19, 15, 54, 41, 902538)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2019, 7, 19, 15, 54, 41, 902516)),
        ),
    ]