# Generated by Django 2.2.4 on 2019-12-11 04:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0015_auto_20191210_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 12, 11, 0, 8, 59, 66206)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2019, 12, 11, 0, 8, 59, 66206)),
        ),
    ]
