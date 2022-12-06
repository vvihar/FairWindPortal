# Generated by Django 3.2.15 on 2022-12-01 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventReflection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reflection', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reflections', to='events.event', verbose_name='イベント')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reflections', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': '振り返り',
                'verbose_name_plural': '振り返り',
                'unique_together': {('event', 'user')},
            },
        ),
    ]
