# Generated by Django 3.2.15 on 2022-08-27 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_schooldetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schooldetail',
            name='id',
        ),
        migrations.AddField(
            model_name='schooldetail',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='備考'),
        ),
        migrations.AlterField(
            model_name='schooldetail',
            name='school',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='detail', serialize=False, to='events.school', verbose_name='学校'),
        ),
    ]
