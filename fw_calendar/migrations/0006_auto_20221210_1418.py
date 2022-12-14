# Generated by Django 3.2.16 on 2022-12-10 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fw_calendar', '0005_schedule_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'スケジュール', 'verbose_name_plural': 'スケジュール'},
        ),
        migrations.AddField(
            model_name='schedule',
            name='no_delete',
            field=models.BooleanField(default=False, verbose_name='削除不可'),
        ),
    ]
