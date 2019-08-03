# Generated by Django 2.2.1 on 2019-08-03 04:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0016_auto_20190802_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendaserv',
            name='descuento',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_fin',
            field=models.TimeField(blank=True, default=datetime.datetime(2019, 8, 3, 0, 3, 6, 148340)),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='hora_inicio',
            field=models.TimeField(default=datetime.datetime(2019, 8, 3, 0, 3, 6, 148320)),
        ),
    ]
