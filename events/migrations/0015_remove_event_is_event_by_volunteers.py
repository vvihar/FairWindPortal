# Generated by Django 3.2.15 on 2022-09-28 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20220901_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_event_by_volunteers',
        ),
    ]
