# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-15 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_billet_canceled'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationGrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='quantité')),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='selling_mode',
            field=models.CharField(choices=[('P', "Public (en fonction de l'évènemenet"), ('I', 'Sur invitation direct'), ('L', 'Verrouillé')], default='P', max_length=1, verbose_name='mode de vente'),
        ),
        migrations.AddField(
            model_name='product',
            name='selling_mode',
            field=models.CharField(choices=[('P', "Public (en fonction de l'évènemenet"), ('I', 'Sur invitation direct'), ('L', 'Verrouillé')], default='P', max_length=1, verbose_name='mode de vente'),
        ),
        migrations.AddField(
            model_name='invitationgrant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produit', to='api.Product'),
        ),
    ]
