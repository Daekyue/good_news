# Generated by Django 4.2.16 on 2024-11-21 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_newsarticle_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='url',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]