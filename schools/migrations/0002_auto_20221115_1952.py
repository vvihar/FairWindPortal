# Generated by Django 3.2.15 on 2022-11-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日時'),
        ),
        migrations.AddField(
            model_name='school',
            name='memo',
            field=models.TextField(default='', verbose_name='メモ'),
        ),
        migrations.DeleteModel(
            name='SchoolDetail',
        ),
    ]
