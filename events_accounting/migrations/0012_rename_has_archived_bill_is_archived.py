# Generated by Django 3.2.15 on 2022-11-19 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_accounting', '0011_bill_has_archived'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='has_archived',
            new_name='is_archived',
        ),
    ]
