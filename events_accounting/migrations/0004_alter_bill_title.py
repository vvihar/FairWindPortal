# Generated by Django 3.2.15 on 2022-11-19 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_accounting', '0003_bill_payment_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='件名'),
        ),
    ]