# Generated by Django 3.1.14 on 2023-03-07 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20230307_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
    ]
