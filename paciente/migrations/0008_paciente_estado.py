# Generated by Django 2.1.4 on 2019-07-22 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0007_auto_20190722_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
