# Generated by Django 3.2.16 on 2022-12-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fw_calendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.TimeField(default='21:28', verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(default='20:28', verbose_name='開始時間'),
        ),
    ]
