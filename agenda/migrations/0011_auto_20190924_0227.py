# Generated by Django 2.2.4 on 2019-09-24 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0010_auto_20190917_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 9, 24, 2, 27, 38, 878673)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2019, 9, 24, 2, 27, 38, 878673)),
        ),
    ]
