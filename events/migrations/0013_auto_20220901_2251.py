# Generated by Django 3.2.15 on 2022-09-01 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_alter_event_group_in_charge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_datetime',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_datetime',
        ),
    ]