# Generated by Django 2.2.4 on 2019-09-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0010_auto_20190917_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivopdf',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]
