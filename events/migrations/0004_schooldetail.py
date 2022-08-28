# Generated by Django 3.2.15 on 2022-08-27 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_school_prefecture'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='detail', to='events.school', verbose_name='学校')),
            ],
        ),
    ]
