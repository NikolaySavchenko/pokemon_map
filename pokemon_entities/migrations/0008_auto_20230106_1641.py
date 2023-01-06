# Generated by Django 3.1.14 on 2023-01-06 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0007_auto_20230106_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
        migrations.RemoveField(
            model_name='pokemon',
            name='previous_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='possible_evolutions', to='pokemon_entities.pokemon'),
        ),
    ]
