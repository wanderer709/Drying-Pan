# Generated by Django 4.0.1 on 2022-04-12 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0009_remove_pokemon_type1_remove_pokemon_type2'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='type1',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='type2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
