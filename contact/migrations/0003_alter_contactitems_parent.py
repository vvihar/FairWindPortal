# Generated by Django 3.2.16 on 2022-12-14 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20221214_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactitems',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='contact.contactitems', verbose_name='親コメント'),
        ),
    ]
