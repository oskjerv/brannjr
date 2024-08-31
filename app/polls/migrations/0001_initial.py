# Generated by Django 5.1 on 2024-08-30 17:53

import django.db.models.deletion
import polls.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent', models.CharField(default=None)),
                ('date', models.DateTimeField(verbose_name='Kampdato')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('opponent', 'date'), name='unique_opponent_date')],
            },
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('shirt_no', models.IntegerField(default=None)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('name', 'shirt_no'), name='unique_name_shirtno')],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('GK', 'Målvakt'), ('LB', 'Venstreback'), ('RB', 'Høyreback'), ('LCB', 'Venstre midtstopper'), ('RCB', 'Høyre midtstopper'), ('LDM', 'Venstre defensiv midtbane'), ('HDM', 'Høyre defensiv midtbane'), ('LCM', 'Venstre sentral midtbane'), ('RCM', 'Høyre sentral midtbane'), ('LW', 'Venstreving'), ('RW', 'Høyreving'), ('LAM', 'Venstre offensiv midtbane'), ('RAM', 'Høyre offensiv midtbane'), ('LCF', 'Venstre spiss'), ('RCF', 'Høyre spiss')], max_length=200)),
                ('goals', models.IntegerField(blank=True, default=0, null=True, validators=[polls.models.validate_non_negative])),
                ('assists', models.IntegerField(blank=True, default=0, null=True, validators=[polls.models.validate_non_negative])),
                ('started', models.BooleanField(blank=True, default=True, null=True)),
                ('subbed', models.BooleanField(blank=True, default=False, null=True)),
                ('rating', models.IntegerField(default=0, validators=[polls.models.validate_rating])),
                ('mom_votes', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.squad')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('match', 'player'), name='unique_match_player')],
            },
        ),
    ]
