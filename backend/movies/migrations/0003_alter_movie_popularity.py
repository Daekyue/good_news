# Generated by Django 4.2.16 on 2024-11-21 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]