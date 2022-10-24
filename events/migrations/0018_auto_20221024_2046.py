# Generated by Django 3.2.15 on 2022-10-24 11:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0017_auto_20221024_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants_declined',
            field=models.ManyToManyField(blank=True, related_name='event_declined', to=settings.AUTH_USER_MODEL, verbose_name='打診の辞退者'),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants_invited',
            field=models.ManyToManyField(blank=True, related_name='event_invited', to=settings.AUTH_USER_MODEL, verbose_name='打診中の参加者'),
        ),
    ]