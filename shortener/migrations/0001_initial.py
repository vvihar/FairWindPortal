# Generated by Django 3.2.15 on 2022-11-16 16:44

from django.db import migrations, models
import shortener.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('hashid', models.CharField(default=shortener.models.generate_unique_hashid, editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('redirect_to', models.TextField(unique=True, verbose_name='リダイレクト先のパス')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='タイトル')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
            ],
            options={
                'verbose_name': '短縮URL',
                'verbose_name_plural': '短縮URL',
            },
        ),
    ]