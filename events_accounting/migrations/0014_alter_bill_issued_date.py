# Generated by Django 3.2.15 on 2022-11-19 04:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_accounting', '0013_remove_bill_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='issued_date',
            field=models.DateField(default=datetime.date.today, verbose_name='発行日'),
        ),
    ]
