# Generated by Django 3.1.14 on 2023-01-07 17:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0016_auto_20230107_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Появился в:'),
            preserve_default=False,
        ),
    ]
