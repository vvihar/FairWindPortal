# Generated by Django 3.2.15 on 2022-11-19 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_accounting', '0012_rename_has_archived_bill_is_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='title',
        ),
    ]
