# Generated by Django 3.2.15 on 2022-11-21 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_accounting', '0017_auto_20221120_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
        ),
    ]