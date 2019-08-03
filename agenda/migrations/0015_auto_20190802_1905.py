# Generated by Django 2.2.1 on 2019-08-02 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0014_auto_20190802_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='ddc1',
            field=models.CharField(choices=[('J1', 'J1'), ('J2', 'J2'), ('J3', 'J3'), ('J4', 'J4'), ('J5', 'J5')], default='J1', max_length=50),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 8, 2, 19, 5, 31, 638864)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2019, 8, 2, 19, 5, 31, 638841)),
        ),
    ]
