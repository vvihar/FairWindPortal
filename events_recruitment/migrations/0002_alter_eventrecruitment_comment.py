# Generated by Django 3.2.15 on 2022-11-15 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventrecruitment',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='コメント'),
        ),
    ]
